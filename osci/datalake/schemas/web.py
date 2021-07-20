from .public import OSCIChangeRankingSchema


class WebOSCIChangeRankingData:
    class Columns:
        position = 'position'
        position_change = 'positionChange'
        company = 'company'
        active = 'activeContributors'
        active_change = 'activeContributorsChange'
        total = 'totalCommunity'
        total_change = 'totalCommunityChange'
        year_of_year = 'yoy'
        languages = 'languages'
        licenses = 'licenses'
        contributors = 'contributors'

    mapping = {
        OSCIChangeRankingSchema.position: Columns.position,
        OSCIChangeRankingSchema.position_change: Columns.position_change,
        OSCIChangeRankingSchema.company: Columns.company,
        OSCIChangeRankingSchema.active: Columns.active,
        OSCIChangeRankingSchema.active_change: Columns.active_change,
        OSCIChangeRankingSchema.total: Columns.total,
        OSCIChangeRankingSchema.total_change: Columns.total_change
    }


class WebOSCIChangeRanking:
    class Columns:
        date = 'date'
        compared_date = 'comparedDate'
        data = 'data'
