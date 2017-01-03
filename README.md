# Nosedive - Inspired by Black Mirror S03E01

The website [Nosedive](https://nosedive.space) is a parody of Black Mirror S03E01 Nosedive. It calculates a Nosedive rating based on your history on Facebook.

## How Does It Work?

It grabs a user's posts and reactions thereof to calculate her rating. The Nosedive rating consists of two parts:

1. The base score: the popularity of the user. Since the "reaction" on Facebook is neutral, there is no way to get an inference of a numerical rate merely from the "reactions" from a post. Therefore, it uses popularity as an approximation of the "rating" concept in the show.
2. The bonus score: high-rate-user effect. In the show, the higher the rating of your friend is, the more powerful he/she is. It would be cumbersome to recursively calculate a complete Nosedive rating. In the implementation, it takes the base score as the weight of a user.

See the implementation in the `algorithm.py`

## Privacy

You can check `algorithm.py` to see what data does it store in the database.

If you have any concern, there is a way to remove it: simply call `/remove/your_id` with valid access token and your data will be removed from the database.

## Credits

The main front-end is taken from Ahmed Tarek (http://codepen.io/ahmedtarek2134/pen/ggYmXp).

The odometer is taken from Benjamin (http://codepen.io/maggiben/pen/nmIso)

Everything else is licensed under GPLv3 License unless stated elsewhere.

