from django import template

register = template.Library()

@register.simple_tag
def if_voted_on_reading_list(reading_list,
                             relevant_votes,
                             points_to_check,
                             text_if_voted,
                             text_if_not_voted):

    # Find if the user voted on this reading list:
    for vote in relevant_votes:
        if vote.reading_list == reading_list:
            # If they did, then check if they voted the same way as
            # "points_to_check", otherwise show nothing
            if vote.points == points_to_check:
                return text_if_voted
            else:
                return text_if_not_voted

    # Didn't vote on this at all, by default show text_if_not_voted
    return text_if_not_voted

