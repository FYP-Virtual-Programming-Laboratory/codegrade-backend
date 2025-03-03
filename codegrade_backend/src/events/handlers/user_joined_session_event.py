from src.events.handlers.base import AbstractLifeCycleEventHandler
from src.events.handlers.schemas import UserJoinedSessionEventData
from sqlmodel import select
from src.models import Session, User



class UserJoinedSessionEventHandler(AbstractLifeCycleEventHandler):
    """Handler for user joined session events."""
    
    def _get_session(self, external_session_id: str) -> Session:
        """Get the session."""
        return self.db_session.exec(
            select(Session).where(
                Session.external_id == external_session_id,
                Session.is_active == True,  # Only active sessions are considered
            )
        ).one()

    def _get_user(
        self, 
        session: Session,
        event_data: UserJoinedSessionEventData,
    ) -> User:
        """Get the user by external ID."""
        return self.db_session.exec(
            select(User).where(
                external_id=event_data.external_user_id,
                session_id=session.id,
            )
        )

    def handle_event(
        self,
        external_session_id: str,
        event_data: UserJoinedSessionEventData,
    ) -> None:
        """Handle the event data."""
        session = self._get_session(external_session_id)
        user = self._get_user(session=session, event_data=event_data)
        user.fullname = event_data.fullname
        self.db_session.add(user)
        self.db_session.commit()
