from datetime import datetime
from typing import (
    Annotated,
    Literal
)
from uuid import UUID

from sqlalchemy import (
    String,
    BigInteger,
    DateTime,
    Enum,
    text
)
from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column
)

guid_pk = Annotated[
    UUID,
    mapped_column(
        primary_key=True,
        index=True,
        server_default=text("gen_random_uuid()")
    )
]

str_128 = Annotated[
    str,
    mapped_column(
        String(128),
        server_default=""
    )
]

str_128_pk = Annotated[
    str,
    mapped_column(
        String(128),
        primary_key=True
    )
]

str_512 = Annotated[
    str,
    mapped_column(
        String(512),
        server_default=""
    )
]

str_1024 = Annotated[
    str,
    mapped_column(
        String(1024),
        server_default=""
    )
]

unique_str_128 = Annotated[
    str,
    mapped_column(String(128), unique=True)
]

unique_int = Annotated[
    int,
    mapped_column(unique=True)
]

created_at = Annotated[
    datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
]

updated_at = Annotated[
    datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
]

true = Annotated[
    bool,
    mapped_column(
        server_default="true",
        index=True
    )
]

false = Annotated[
    bool,
    mapped_column(
        server_default="false",
        index=True
    )
]

session_role = Annotated[
    Literal["Leader", "Member"],
    mapped_column(
        Enum(
            "Leader",
            "Member",
            "",
            name="session_role_enum"
        ),
        server_default=""
    )
]

lobby_state = Annotated[
    Literal[
        "Preparing",
        "AllJoined",
        "InvitesSent",
        "InvitesAccepted",
        "MembersLoaded",
        "SearchStarted"
    ],
    mapped_column(
        Enum(
            "Preparing",
            "AllJoined",
            "InvitesSent",
            "InvitesAccepted",
            "MembersLoaded",
            "SearchStarted",
            name="lobby_state_enum"
        ),
        server_default="Preparing"
    )
]

game_state = Annotated[
    Literal[
        "Preparing",
        "Confirmed"
    ],
    mapped_column(
        Enum(
            "Preparing",
            "Confirmed",
            name="game_state_enum"
        ),
        server_default="Preparing"
    )
]


class Base(DeclarativeBase):
    type_annotation_map = {
        int: BigInteger,
        datetime: DateTime(timezone=True)
    }
