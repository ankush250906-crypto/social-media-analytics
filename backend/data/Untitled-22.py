# backend/app/api/reports.py
from fastapi import APIRouter, Depends, status
from app.auth import get_current_user
from app.tasks import generate_campaign_pdf_report

router = APIRouter(prefix="/api/v1/reports", tags=["Reports"])

@router.post("/trigger-pdf", status_code=status.HTTP_202_ACCEPTED)
def trigger_pdf_report(current_user = Depends(get_current_user)):
    """Trigger background generation of campaign performance PDF report."""
    task = generate_campaign_pdf_report.delay("social_media_analytics_report.pdf")
    return {
        "message": "PDF report generation task dispatched successfully.",
        "task_id": task.id
    }