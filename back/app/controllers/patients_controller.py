import base64
import binascii
from pathlib import Path
from uuid import uuid4
import sys
import os
from fastapi import Body, FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from app.dal.proxy import Proxy
from app.entities.requests.patient_request import PatientRequest
from app.interfaces.controller import Controller

# Add parent directory to sys.path to ensure relative imports work correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class PatientsController(Controller):
    """
    Controller class for managing patients through FastAPI.
    """

    _instance = None

    @classmethod
    def get_app(cls):
        """
        Singleton method to get or create an instance of the FastAPI application.

        Returns:
        FastAPI: An instance of the FastAPI application.
        """
        if cls._instance is None:
            cls._instance = cls._create_instance()
        return cls._instance

    @classmethod
    def _create_instance(cls):
        """
        Private method to create a new instance of the FastAPI application.

        Returns:
        FastAPI: A new instance of the FastAPI application.
        """
        app = FastAPI(debug=True)

        proxy_instance = Proxy()
        account_db_instance = proxy_instance.account_db

        # Configure CORS middleware for cross-origin requests
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Replace "*" with your specific origins if needed
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE"],
            allow_headers=["Content-Type", "Authorization"],
        )

        # Summary explaining the controllers
        """
        This FastAPI application provides endpoints for various functionalities including account management, dataset management, preprocessing, model training, and patient risk assessment. Each controller is categorized based on its functionality.
        """

        # Endpoint to create a patient
        @app.post("/create-patient", tags=["Controller Patients"], summary="Create Patient")
        async def create_patient(patient_data: PatientRequest):            
            """
            Endpoint to create a new patient.

            Args:
            full_name (str): The name of the patient.
            age (int): The age of the patient.
            image (str): Image of the patient.
            phone_number (str): The phone number of the patient.
            email (str): Email address of the patient.
            doctor_id (int): ID of the doctor associated with the patient.

            Returns:
            dict: A dictionary with a message indicating the success of the operation.

            Raises:
            HTTPException: If there is an error creating the patient.
            """
            try:
                try:
                    header, base64_data = patient_data.image.split('base64,', 1)
                    if not header.startswith('data:image/'):
                        raise ValueError('Expected an image data URL')
                    image_data = base64.b64decode(base64_data, validate=True)
                except (ValueError, binascii.Error) as exc:
                    raise HTTPException(status_code=422, detail="Invalid patient image") from exc
                image_dir = Path(__file__).resolve().parents[1] / 'dal' / 'images'
                image_dir.mkdir(parents=True, exist_ok=True)
                file_name = f'{uuid4().hex}.jpg'
                file_path = image_dir / file_name
                file_path.write_bytes(image_data)
                try:
                    account_db_instance.create_patient(patient_data.name, patient_data.age, patient_data.phone_number, file_name, patient_data.email, patient_data.doctor_id)
                except Exception:
                    file_path.unlink(missing_ok=True)
                    raise
                return {"message": "Patient created successfully"}
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error creating patient: {e}")
            
        def load_image_as_base64(image_path):
            with open(image_path, 'rb') as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
            
        # Endpoint to get patients by doctor ID
        @app.get("/get-patients/{doctor_id}", tags=["Controller Patients"], summary="Get Patients by Doctor ID")
        def get_patients_by_doctor_id(doctor_id: int):
            try:
                patients = account_db_instance.get_patients_by_doctor_id(doctor_id)
                if not patients:
                    return []

                modified_patients = []
                for patient in patients:
                    image_path = Path(__file__).resolve().parents[1] / 'dal' / 'images' / Path(patient[5] or '').name
                    if image_path.is_file():
                        image_binary = load_image_as_base64(image_path)
                        new_patient = patient[:5] + (image_binary,) + patient[6:]
                        modified_patients.append(new_patient)
                    else:
                        print(f"Image not found for patient: {patient[1]}")
                        modified_patients.append(patient[:5] + ("",) + patient[6:])
    
                return modified_patients
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error retrieving patients: {e}")

        # Endpoint to update a patient
        @app.put("/update-patient/{patient_id}", tags=["Controller Patients"], summary="Update Patient")
        def update_patient(patient_id: int, name: str, description: str, imagePath: str, email: str, doctor_id: int):
            """
            Endpoint to update patient details.

            Args:
            patient_id (int): The ID of the patient to update.
            name (str): The updated name of the patient.
            description (str): The updated description of the patient.
            imagePath (str): The updated image path of the patient.
            email (str): The updated email address of the patient.
            doctor_id (int): The updated ID of the doctor associated with the patient.

            Returns:
            dict: A dictionary with a message indicating the success of the operation.

            Raises:
            HTTPException: If there is an error updating the patient.
            """
            try:
                account_db_instance.update_patient(name, description, imagePath, email, doctor_id, patient_id)
                return {"message": "Patient updated successfully"}
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error updating patient: {e}")

        # Endpoint to delete a patient
        @app.delete("/delete-patient/{patient_id}", tags=["Controller Patients"], summary="Delete Patient")
        def delete_patient(patient_id: int):
            """
            Endpoint to delete a patient.

            Args:
            patient_id (int): The ID of the patient to delete.

            Returns:
            dict: A dictionary with a message indicating the success of the operation.

            Raises:
            HTTPException: If there is an error deleting the patient.
            """
            try:
                account_db_instance.delete_patient(patient_id)
                return {"message": "Patient deleted successfully"}
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error deleting patient: {e}")

        # Endpoint for health check
        @app.get("/health", tags=["Health Check"], summary="Health Check")
        def health_check():
            """
            Health check endpoint to verify the service is running.

            Returns:
            dict: A dictionary indicating the health status of the service.
            """
            return {"status": "ok", "message": "Service is up and running"}

        return app