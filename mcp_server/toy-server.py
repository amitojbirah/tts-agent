from pathlib import Path
import pandas as pd
from mcp.server.mcpserver import MCPServer




mcp=MCPServer("windsor-toy")
csv_path = Path(__file__).resolve().parent.parent / "toy-data.csv"
df = pd.read_csv(csv_path)

@mcp.tool()
def get_schema()-> dict[str,str]:
    """get_schema called"""
    return df.dtypes.astype(str).to_dict()


@mcp.tool()
def get_row_count() -> int:
    """Returns the total number of rows currently loaded in the dataset."""
    return len(df)


@mcp.tool()
def filter_data(column: str, value: str, limit: int = 10) -> list[dict]:
    """
    Filters the dataset to rows where the specified column matches the given value.

    column: The name of the column to filter on. Must be one of the dataset's column names.
    value: The exact value to search for within the specified column.
    limit: The maximum number of records to return (defaults to 10).
    """
    if column not in df.columns:
        raise ValueError(f"Invalid column '{column}'. Valid columns are: {list(df.columns)}")
        
    row_filter = df[column].astype(str) == value
    filtered_df = df[row_filter]
    
    return filtered_df.head(limit).fillna("").to_dict(orient="records")

@mcp.resource("windsor://about")
def get_data() :
    """Returns the entire dataset as a list of dictionaries."""
    return "data set is about complaints in windsor"

@mcp.resource("windsor://ward/{ward}")
def ward_summary(ward: str)->str:
    """Returns a summary of complaints for a specific ward."""
    ward="WARD "+ward
    ward_df = df[df['Ward'].astype(str) == ward]
    count=len(ward_df)
    return f"Ward {ward} has {count} complaints."
if __name__ == "__main__":
    mcp.run()

