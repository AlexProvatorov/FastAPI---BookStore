"""02_add_goods_model

Revision ID: d34b46f778c6
Revises: e1409acaf101
Create Date: 2024-04-19 16:40:18.506326

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d34b46f778c6"
down_revision: Union[str, None] = "e1409acaf101"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "authors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("cost", sa.DECIMAL(), nullable=False),
        sa.Column("count_in_stock", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "time_created",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("time_updated", sa.DateTime(timezone=True), nullable=True),
        sa.Column("photo", sa.String(), nullable=False),
        sa.Column("date_released", sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_table(
        "tags",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_table(
        "authors_of_books",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("id_book", sa.Integer(), nullable=True),
        sa.Column("id_author", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["id_author"],
            ["tags.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_book"],
            ["books.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "tags_of_books",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("id_book", sa.Integer(), nullable=True),
        sa.Column("id_tag", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["id_book"],
            ["books.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_tag"],
            ["tags.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("tags_of_books")
    op.drop_table("authors_of_books")
    op.drop_table("tags")
    op.drop_table("books")
    op.drop_table("authors")
    # ### end Alembic commands ###
