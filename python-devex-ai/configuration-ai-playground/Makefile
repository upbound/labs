lint:	# Ruff check Python files
	ruff check ./functions/compose-network/igw.py
	ruff check ./functions/compose-network/main.py
	ruff check ./functions/compose-network/rt.py
	ruff check ./functions/compose-network/sg.py
	ruff check ./functions/compose-network/subnets.py
	ruff check ./functions/compose-network/vpc.py

connect: # Connect to an instance
	ssh ubuntu@$$(kubectl get instance huggingface-deep-learning-neuron-markus-schweig -o jsonpath='{.status.atProvider.publicIp}')
