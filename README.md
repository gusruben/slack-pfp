# Slack Profile Picture Randomizer

This is a tiny Python program (<75 LoC) to randomize my profile picture on Slack every 30 minutes. Here's how you can set it up yourself:

## Setup Instructions

### Creating a Slack App

1. Go to [api.slack.com/apps](https://api.slack.com/apps) and create a new app. Choose "from scratch" and call it whatever you want
2. Under "OAuth & Permissions," add the User Token Scope `users.profile:write`
3. Click "Install App to Workspace"
4. Copy the OAuth token from the "User OAuth Token" box (starts with `xoxp-`)

### Running the Program

1. Clone the repository
2. Install the dependencies with `pip install -r requirements.txt` (requires Python 3.7+ with pip)
3. Copy `.env.example` to `.env`, and add in the OAuth token to `USER_TOKEN`
4. Place all your images in the folder called `images` (and clear out the example images if you'd like)
5. Run the program with `python main.py`

> This program was developed with [uv](https://github.com/astral-sh/uv)! if you'd like to hack on it, it's recommended you use uv as well.