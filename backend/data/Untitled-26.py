# backend/app/api/campaigns.py (updates)
from app.auth import get_current_user, require_role

@router.post("/", response_model=CampaignMetricResponse, status_code=status.HTTP_201_CREATED)
def create_campaign(
    payload: CampaignMetricCreate, 
    db: Session = Depends(get_db), 
    current_user = Depends(require_role("admin"))  # Restrict to Admin only!
):
    # Creation logic...