# Discord-bot
This Discord bot is developed using Python and offers a wide range of features for managing voice channels and facilitating team-based games.


# Discord Bot for Room Management and Team Generation

## Overview

This Discord bot is designed to facilitate room management and team-based gaming within a Discord server. It provides users with a range of tools to create and manage temporary voice channels, as well as utilities for organizing players into random teams for games. Additionally, the bot includes features for creating tickets for reporting issues or making purchase requests.

## Features

### Room Management

Users can create and manage their own temporary voice channels with the following commands:

- **🚫 Ban/Unban**: Ban or unban a user from the voice channel.
- **➕ Set User Limit**: Set a limit on the number of users who can join the channel.
- **🔒 Lock/Unlock**: Lock or unlock the voice channel.
- **✍️ Rename Room**: Change the name of the voice channel.
- **🏌 Kick User**: Kick a user from the voice channel.
- **🔇 Mute/Unmute**: Mute or unmute a user in the voice channel.

### Team Generation

The bot can randomly divide users into two teams for games:

- **Team Generation**: Users can join a pool, and once the desired number of participants is reached, the bot randomly splits them into two teams.
- **Team Management**: The bot creates separate voice channels for each team and automatically moves users to their respective channels.

### Ticket System

Users can create tickets for admins to handle:

- **Create Ticket**: Users can report issues or make requests by creating a ticket that will be sent to the server's admins.

## Setup

### Prerequisites

- Python 3.8+
- Discord.py library

### Installation

1. Clone this repository to your local machine.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your bot's token in the `settings.py` file.

### Running the Bot

To start the bot, run:

```bash
python bot.py
```

### Folder Structure

- **bot.py**: The main bot file, handling core functionalities.
- **buttons.py**: Handles the interaction with Discord buttons for team generation and room management.
- **coggg.py**: Manages the room controls (ban, kick, mute, etc.) via buttons.
- **settings.py**: Contains configuration settings and utilities for database management.

## Commands

- **Room Management**: Use `-ewq` to display room management controls.
- **Team Generation**: Use `-teamgenerate` to initiate team generation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contribution

Feel free to contribute to this project by forking the repository and submitting a pull request. Please ensure your code follows the existing style and structure.

---
