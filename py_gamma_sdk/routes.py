# File to holder/store API routes

# Sports routes
SPORTS = "/sports"
SPORTS_TEAMS = "/sports/teams"
SPORTS_MARKET_TYPES = "/sports/market-types"

# Tags routes
TAGS = "/tags"
TAGS_BY_ID = "/tags/{tag_id}"
TAGS_BY_SLUG = "/tags/slug/{slug}"
TAGS_RELATED_BY_ID = "/tags-related-tag-id/{tag_id}"
TAGS_RELATED_BY_SLUG = "/tags-related-tag-slug/{slug}"
TAGS_RELATED_TO_ID = "/tags/{tag_id}/related"
TAGS_RELATED_TO_SLUG = "/tags/slug/{slug}/related"

# Events routes
EVENTS = "/events"
EVENTS_BY_ID = "/events/{event_id}"
EVENTS_TAGS = "/events/{event_id}/tags"
EVENTS_BY_SLUG = "/events/slug/{slug}"

# Markets routes
MARKETS = "/markets"
MARKETS_BY_ID = "/markets/{market_id}"
MARKETS_TAGS = "/markets/{market_id}/tags"
MARKETS_BY_SLUG = "/markets/slug/{slug}"

# Series routes
SERIES = "/series"
SERIES_BY_ID = "/series/{series_id}"

# Comments routes
COMMENTS = "/comments"
COMMENTS_BY_ID = "/comments/{comment_id}"
COMMENTS_BY_USER = "/comments/user/{address}"

# Profiles routes
PROFILES_BY_ADDRESS = "/profiles/{address}"

# General routes
STATUS = "/status"
SEARCH = "/search"
PUBLIC_SEARCH = "/public-search"
