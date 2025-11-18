import enum

class UserRole(enum.Enum):
    ADMIN = "admin"
    CLINICIAN = "clinician"
    VIEWER = "viewer"