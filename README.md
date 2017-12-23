# HYDT

How You Doin Today?

## Installation

```
python3 setup.py install
```

After the app is installed, you will have `hydt` as an executable.

## Usage

```
hydt $command -arg $argValue
```

### Commands

* `create_database` -- This will create the initial database file
* `score -e "😋"`-- This will return the score for a given set of emoji that are separated by space or comma.
    > {"score": 27.0, "color": "#681e5b", "color_shifted": "#681e5b", "sentiment": 0}
* `user_score -e "😕 🤩 😚" -u 2 -d "12/22/2017" [-n "some notes about the score"]` -- This will get the score for user 1 on 12/22/2017 and save it to the database (the notes will be saved if they are passed in.). This will update an entry for the given user/date combination.
    > {'user': 1, 'date': '2017-12-22', 'data': {'score': 83.0, 'color': '#7fba00', 'color_shifted': '#7fba00', 'sentiment': 0.5}}
* `user_score_range -u 2 -sdate 12/01/2017 -edate 12/31/2017` -- *NOT WORKING YET* This will get all of the user 2's entries for the given date range.

### Notes

The colar is shifted by determining the deltas between each emoji and shifting the luminosity via every pair. While the sentiment is calculated, it is not currently used to generate the final color.

## Data

At this moment the data is living and will be changed.

#### Current Color Values

| Max Value | Color |
| --------- | ---- |
| 16 | '#3a5dae' |
| 32 | '#681e5b' |
| 48 | '#d81e05' |
| 62 | '#00a6d6' |
| 78 | '#e28c05' |
| 100 | '#7fba00' |

#### Current emoji values

| Emoji | Value |
| ------ | ---- |
| 😀 | 80.5 |
| 😃 | 85.5 |
| 😄 | 88.25 |
| 😁 | 90.5 |
| 😆 | 93.25 |
| 😅 | 87.5 |
| 😂 | 96.5 |
| 🤣 | 100 |
| ☺️ | 90.5 |
| 😊 | 90.25 |
| 😇 | 90.25 |
| 🙂 | 81 |
| 🙃 | 47 |
| 😉 | 83.25 |
| 😌 | 85.5 |
| 😍 | 100 |
| 😘 | 90.25 |
| 😗 | 75.25 |
| 😙 | 78.5 |
| 😚 | 84.75 |
| 😋 | 83.25 |
| 😛 | 78.25 |
| 😝 | 76 |
| 😜 | 73.5 |
| 🤪 | 76.33333333 |
| 🤨 | 47 |
| 🧐 | 47.33333333 |
| 🤓 | 79.75 |
| 😎 | 89.5 |
| 🤩 | 99 |
| 😏 | 79 |
| 😒 | 41 |
| 😞 | 26.75 |
| 😔 | 27.5 |
| 😟 | 42 |
| 😕 | 49 |
| 🙁 | 29.75 |
| ☹️ | 8 |
| 😣 | 24.75 |
| 😖 | 17.5 |
| 😫 | 10.75 |
| 😩 | 18.5 |
| 😢 | 14.25 |
| 😭 | 46.5 |
| 😤 | 27.75 |
| 😠 | 18.25 |
| 😡 | 8.75 |
| 🤯 | 9 |
| 😳 | 40.25 |
| 😱 | 35.5 |
| 😨 | 25 |
| 😰 | 14.75 |
| 😥 | 20.75 |
| 😓 | 40.25 |
| 🤗 | 83.25 |
| 🤔 | 48 |
| 🤭 | 56.66666667 |
| 🤫 | 80 |
| 🤥 | 33.5 |
| 😶 | 39.5 |
| 😐 | 42.5 |
| 😑 | 28 |
| 😬 | 35 |
| 🙄 | 17 |
| 😯 | 46.66666667 |
| 😦 | 34 |
| 😧 | 26.33333333 |
| 😮 | 51.33333333 |
| 😲 | 57 |
| 😴 | 38 |
| 🤤 | 83.75 |
| 😪 | 40 |
| 😵 | 36.33333333 |
| 🤐 | 32.66666667 |
| 🤢 | 5.333333333 |
| 🤮 | 1 |
| 🤧 | 32.66666667 |
| 😷 | 31.66666667 |
| 🤒 | 16.66666667 |
| 🤕 | 11.33333333 |
| 🤑 | 94.33333333 |
| 🤠 | 85 |
| 😾 | 48.33333333 |
| 😿 | 39.66666667 |
| 🙀 | 65.33333333 |
| 😽 | 92.66666667 |
| 😼 | 94.66666667 |
| 😻 | 100 |
| 😹 | 91.66666667 |
| 😸 | 88.33333333 |
| 😺 | 83.33333333 |
| 🎃 | 76.33333333 |
| 🤖 | 78.33333333 |
| 👾 | 73.33333333 |
| 👽 | 76.66666667 |
| ☠️ | 63.33333333 |
| 💀 | 36 |
| 👻 | 63.33333333 |
| 💩 | 9 |
| 🤡 | 14.66666667 |
| 👺 | 33.66666667 |
| 👹 | 38.33333333 |
| 👿 | 41 |
| 😈 | 71.66666667 |
