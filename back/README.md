### ML Project ###
doctor1@example.com
password1

admin1@example.com





For statring the AdminAPI:
Run: uvicorn AdminAPI.DatasetOps:app --reload
Then go to: http://127.0.0.1:8000/docs for the swagger

POC:

Classification Report:
              precision    recall  f1-score   support

       False       1.00      1.00      1.00        32

    accuracy                           1.00        32
   macro avg       1.00      1.00      1.00        32
weighted avg       1.00      1.00      1.00        32


Accuracy: 
The accuracy of 1.0 (or 100%) means that the model correctly classified all instances in the test set. In other words, there were no misclassifications.
Precision: Precision measures the proportion of correctly predicted positive instances out of all instances predicted as positive. In this case, the precision for the class labeled as 'False' is 1.00. It means that all instances predicted as 'False' were indeed 'False'. There were no false positives.
Recall:
Recall, also known as sensitivity, measures the proportion of actual positive instances that were correctly predicted by the model. The recall for the class labeled as 'False' is 1.00, indicating that all actual 'False' instances were correctly predicted by the model. There were no false negatives.
F1-score:
The F1-score is the harmonic mean of precision and recall. It provides a balance between precision and recall. A perfect F1-score of 1.00 for the class labeled as 'False' indicates an ideal balance between precision and recall.
Support:
Support refers to the number of actual occurrences of each class in the test set. In this case, there were 32 instances of the class labeled as 'False' in the test set.
Macro avg:
The macro average calculates the average precision, recall, and F1-score across all classes without considering class imbalance. Since there is only one class ('False') in your report, the macro average values are the same as the values for that class.
Weighted avg:
The weighted average calculates the weighted average precision, recall, and F1-score, taking into account the number of instances for each class. In this case, since there is only one class, the weighted average values are also the same as the values for that class.
Overall, the results indicate that your model performed perfectly on the test set, achieving 100% accuracy and providing precise and reliable predictions for the class labeled as 'False'.





queries:
'''
-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(50),
    password VARCHAR(50),
    role INT -- 1 doctor 2 admin
);

-- Create patients table
CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    phone_number VARCHAR(15),
    full_name VARCHAR(50),
    age INT,
    photo VARCHAR(255),
    doctor_id INT
);

-- Insert admins
INSERT INTO users (email, name, password, role)
VALUES
    ('admin1@example.com', 'Admin 1', 'password1', 2),
    ('admin2@example.com', 'Admin 2', 'password2', 2),
    ('admin3@example.com', 'Admin 3', 'password3', 2);

-- Insert doctors
INSERT INTO users (email, name, password, role)
VALUES
    ('doctor1@example.com', 'Doctor 1', 'password1', 1),
    ('doctor2@example.com', 'Doctor 2', 'password2', 1),
    ('doctor3@example.com', 'Doctor 3', 'password3', 1);

-- Insert patients
-- Patients for Doctor 1 (assuming doctor_id 1)
INSERT INTO patients (email, phone_number, full_name, age, photo, doctor_id)
VALUES
    ('patient1_doc1@example.com', '123456789', 'John Doe', 30, 'patient1_doc1@example.com.jpg', 4),
    ('patient2_doc1@example.com', '987654321', 'Jane Smith', 25, 'patient2_doc1@example.com.jpg', 4),
    ('patient3_doc1@example.com', '555666777', 'Alice Green', 28, 'patient3_doc1@example.com.jpg', 4),
    ('patient4_doc1@example.com', '888999000', 'Bob Black', 32, 'patient4_doc1@example.com.jpg', 4),
    ('patient5_doc1@example.com', '333444555', 'Charlie Yellow', 27, 'patient5_doc1@example.com.jpg', 4);

-- Patients for Doctor 2 (assuming doctor_id 2)
INSERT INTO patients (email, phone_number, full_name, age, photo, doctor_id)
VALUES
    ('patient1_doc2@example.com', '111222333', 'Michael Johnson', 35, 'patient1_doc2@example.com.jpg', 5),
    ('patient2_doc2@example.com', '444555666', 'Emily Davis', 40, 'patient2_doc2@example.com.jpg', 5);

-- Patients for Doctor 3 (assuming doctor_id 3)
INSERT INTO patients (email, phone_number, full_name, age, photo, doctor_id)
VALUES
    ('patient1_doc3@example.com', '777888999', 'David Brown', 45, 'patient1_doc3@example.com.jpg', 6),
    ('patient2_doc3@example.com', '000111222', 'Sarah White', 50, 'patient2_doc3@example.com.jpg', 6);
'''
