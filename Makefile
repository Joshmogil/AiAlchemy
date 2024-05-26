dev-init:
	@echo "\033[0;32mSetting up development environment...\033[0m"
	cd ai-alchemy && poetry install
	@echo "\033[0;32mCreating .env file...\033[0m"
	echo "OPENAI_API_KEY=" > .env
	@echo "\033[0;32mPlease add your OpenAI API key to the .env file.\033[0m"
	@echo "\033[0;32mRun the following to finish setting up dev environment: cd ai-alchemy then poetry shell\033[0m"

pull-requests-tests:
	@echo "\033[0;32mRunning tests...\033[0m"
	cd ai-alchemy && poetry run pytest
	@echo "\033[0;32mRunning static type checker...\033[0m"
	cd ai-alchemy && poetry run mypy .