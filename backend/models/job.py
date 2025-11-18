# models/story_job.py
from sqlalchemy import Column, Integer, String, DateTime, Text, Index
from sqlalchemy.sql import func
from db.database import Base

class StoryJob(Base):
    __tablename__ = "story_jobs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(String(255))  
    session_id = Column(String(255))  
    theme = Column(Text)  # Utiliser Text pour les longs textes
    status = Column(String(50))  # Spécifier une longueur raisonnable
    story_id = Column(Integer)
    error = Column(Text)  # Utiliser Text pour les messages d'erreur
    created_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime, nullable=True)

    # Définir l'index avec une longueur spécifique si nécessaire
    __table_args__ = (
        Index('ix_story_jobs_session_id', 'session_id'),
        Index('ix_story_jobs_job_id', 'job_id'),
        Index('ix_story_jobs_status', 'status'),
    )

    def __repr__(self):
        return f"<StoryJob(id={self.id}, job_id={self.job_id}, status={self.status})>"