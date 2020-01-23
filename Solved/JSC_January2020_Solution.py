
def winnable_state(current, prev, memo):
	
	if (current, prev) not in memo:

		if current >= 100:
			memo[(current, prev)] = False

		else:
			if prev == -1: # player is first to act
				memo[(current, prev)] = not any([winnable_state(current + i, current, memo) for i in range(1,11)])

			else:
				memo[(current, prev)] = not any([winnable_state(current + i, current, memo) for i in range(1,11) if current + i - prev != 11])			
	
	return memo[(current, prev)]


memo = {}
winnable_state(0, -1, memo)

print("\nwinning numbers:")

for i in range(1,100):
	if winnable_state(i, -1, memo):
		print(i, ':', winnable_state(i, -1, memo))

"""
Reasoning:
	Whoever goes first (in this case, Nate) will win if they say "3".

	Solution:
	Working backwards, if we can say 99, we win (since anything they say after is a bust).

	I claim that if we can say 87, then we can always win.

	Proof: Suppose we say 87.

	Case 1: They follow with 87+N where 2<=N<=10. Then, we follow that with 87+N+(12-N) to get to 99 (we win).

	Case 2: They follow with 88. Then regardless of what we say after, they are not allowed to follow with 99 (direct violation of the "11 rule"). Thus, they either follow with a number above 99 (we win) or a number less than 99, in which case we can say 99 on the following turn (we win).

	By the same inductive reasoning, if we can say 75, will win. Same goes for 63, 51, 39, 27, 15, and lastly 3.
"""


