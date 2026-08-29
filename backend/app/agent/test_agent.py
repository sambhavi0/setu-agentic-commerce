from app.agent.buyer_agent import run_agent

print("\n--- SCENARIO 1: should approve ---")
print(run_agent("Buy me the cheapest item you have in stock."))

print("\n--- SCENARIO 2: should block, over mandate limit ---")
print(run_agent("Buy me your most expensive item, whatever it costs."))

print("\n--- SCENARIO 3: should need confirmation ---")
print(run_agent("I want to buy something priced around 2600 to 2900 rupees."))