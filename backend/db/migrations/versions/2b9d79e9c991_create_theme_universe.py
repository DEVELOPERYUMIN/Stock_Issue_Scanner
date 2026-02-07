from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "2b9d79e9c991"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "theme_universe",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("theme", sa.String(50), nullable=False, comment="테마명"),
        sa.Column("ticker", sa.String(20), nullable=False, comment="종목코드"),
        sa.Column("stock_name", sa.String(100), nullable=False, comment="종목명"),
        sa.Column("market", sa.String(20), nullable=True, comment="KOSPI/KOSDAQ"),
        sa.Column(
            "created_at",
            sa.DateTime,
            server_default=sa.func.now(),
            nullable=False,
        ),
    )

    # 테마 + 종목코드는 유니크해야 함
    op.create_unique_constraint(
        "uq_theme_universe_theme_ticker",
        "theme_universe",
        ["theme", "ticker"],
    )


def downgrade():
    op.drop_table("theme_universe")
