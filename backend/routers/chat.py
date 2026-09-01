from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from auth import get_current_admin
from database import get_db
from models import Admin, ChatMessage
from schemas import ChatChannelResponse, ChatMessageCreate, ChatMessageResponse

router = APIRouter()

PREDEFINED_CHANNELS = [
    {
        "name": "general",
        "label": "# general",
        "description": "Company-wide announcements, team check-ins, and open discussions.",
        "icon": "💬",
    },
    {
        "name": "engineering",
        "label": "# engineering",
        "description": "Tech discussions, architecture sync, sprint updates, and PR reviews.",
        "icon": "⚡",
    },
    {
        "name": "hr-helpdesk",
        "label": "# hr-helpdesk",
        "description": "Benefits inquiries, leave policies, onboarding help, and workplace support.",
        "icon": "👥",
    },
    {
        "name": "watercooler",
        "label": "# watercooler",
        "description": "Casual chatter, hobby sharing, pet photos, and team fun!",
        "icon": "☕",
    },
]


@router.get("/channels", response_model=List[ChatChannelResponse])
def get_channels(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """List available workplace chat channels."""
    total_staff = db.query(Admin).count()
    return [
        {
            "name": ch["name"],
            "label": ch["label"],
            "description": ch["description"],
            "participant_count": total_staff,
            "icon": ch["icon"],
        }
        for ch in PREDEFINED_CHANNELS
    ]


@router.get("/messages", response_model=List[ChatMessageResponse])
def get_messages(
    channel: str = Query("general"),
    receiver_id: Optional[int] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Retrieve chat message stream for a channel or DM thread."""
    query = db.query(ChatMessage)

    if receiver_id:
        # Direct messaging between current user and target
        query = query.filter(
            (
                (ChatMessage.sender_id == current_admin.id)
                & (ChatMessage.receiver_id == receiver_id)
            )
            | (
                (ChatMessage.sender_id == receiver_id)
                & (ChatMessage.receiver_id == current_admin.id)
            )
        )
    else:
        query = query.filter(
            ChatMessage.channel == channel,
            ChatMessage.message_type == "channel",
        )

    messages = query.order_by(ChatMessage.created_at.asc()).limit(limit).all()
    return messages


@router.post("/messages", response_model=ChatMessageResponse, status_code=status.HTTP_201_CREATED)
def send_message(
    payload: ChatMessageCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Post a message to a channel or direct thread."""
    msg = ChatMessage(
        channel=payload.channel,
        sender_id=current_admin.id,
        sender_name=current_admin.full_name,
        receiver_id=payload.receiver_id,
        message=payload.message.strip(),
        message_type=payload.message_type,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg
