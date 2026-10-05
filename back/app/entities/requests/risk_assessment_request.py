from pydantic import BaseModel, Field, field_validator


class RiskAssessmentRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = ""
    phoneNumber: str = ""
    age: int | None = Field(default=None, ge=0, le=130)
    bloodPressure: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    bloodSugar: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    procedureCount: int | None = Field(default=None, ge=0)
    infectionsReported: int | None = Field(default=None, ge=0)
    bodyTemperature: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    heartRate: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    operativeProcedure: str | None = None
    feelingsAndUrge: str | None = None
    disease: str | None = None
    criticalFeelings: str | None = None
    diseaseRating: int = Field(ge=0, le=5)
    ckdRating: int = Field(ge=0, le=5)
    sirRating: int = Field(ge=0, le=5)
    maRating: int = Field(ge=0, le=5)

    @field_validator("age", "bloodPressure", "bloodSugar", "procedureCount",
                     "infectionsReported", "bodyTemperature", "heartRate",
                     "operativeProcedure", "feelingsAndUrge", "disease",
                     "criticalFeelings", mode="before")
    @classmethod
    def blank_to_none(cls, value):
        return None if isinstance(value, str) and not value.strip() else value
