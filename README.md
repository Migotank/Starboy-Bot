## Overview
A multipurpose Arsenal FC-themed Discord bot! ⚽✨ Features:

⚙️ Utility: Server info, user stats, polls, reminders.

🤖 Automation: Welcome messages, reaction roles, logging.

🔴 Arsenal FC News: Live match updates, team lineups, transfer rumors.

⚽ Football Commands: Fixtures, scores, player stats (via API).

🎉 Fun: Trivia, Saka-themed memes, fan reactions.

## 🤖 Bot Commands

### `!teams [league]`
Lists all teams, or filters by league.

- `!teams` – lists all teams in all leagues.
- `!teams premier league` – lists only Premier League teams.
- `!teams la liga` – lists only La Liga teams.

### `!leagues`
Displays a list of available leagues.


### `!testwelcome` [member]: 
- Manually trigger a welcome message.
- Use this command to simulate the welcome message for any member. Admins only.

### `!serverinfo`
- Displays server statistics such as the server name, owner, member count, roles, and more.

### `!userinfo`[member]:
- Displays information about a specific user or the user who triggered the command.

### `!poll "question" "option1" "option2"` ...:
- Creates a poll with up to 10 options.

### `!remind [time] [reminder]`:  
- Set a reminder with a specified time (e.g., 1h30m Do homework).
- Time format can include days (d), hours (h), and minutes (m).
- The bot will remind you in the specified channel.

### `!kick` [member] [reason]:  (ADMIN/OWNER command)
- Kicks a member from the server with an optional reason.

### `!ban` [member] [reason]:   (ADMIN/OWNER command)
- Bans a member from the server for a specified reason.

### `!unban` [user_id]:   (ADMIN/OWNER command)
- Unbans a user from the server using their user ID.

### `!mute` [member] [reason]:  (ADMIN/OWNER command)
- Mutes a member (requires the 'Muted' role to be set up in the server).

