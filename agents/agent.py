from phidata import PhiApp
from phidata.agent import Agent
from phidata.tools.duckduckgo import DuckDuckGoTool
from phidata.tools.yfinance import YFinanceTool

# Define app
app = PhiApp(name="multi-agentic-ai")

# Define tools
web_tool = DuckDuckGoTool()
finance_tool = YFinanceTool()

# Define a simple agent
assistant = Agent(
    name="assistant",
    tools=[web_tool, finance_tool],
    instructions="You can search the web and fetch stock data.",
)

if __name__ == "__main__":
    print(assistant.run("Find today's news about NVIDIA and current NVDA price."))
