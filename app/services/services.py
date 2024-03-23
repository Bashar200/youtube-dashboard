async def get_youtube_contents(*args, **kwargs):
    db, _, search = args
    page = kwargs["page"]
    page_size = kwargs["page_size"]
    skip = (page - 1) * page_size
    filter_condition = {}
    if search:
        search = search.split(" ")
        title_filter = [{"title": {"$regex": partial_filter, "$options": "i"}} for partial_filter in search]
        description_filter = [{"description": {"$regex": partial_filter, "$options": "i"}} for partial_filter in search]
        filter_condition.update(
            {
                "$or": [
                    *title_filter,
                    *description_filter,
                ]
            }
        )
    res = (
        await db["youtube-details"]
        .find(filter_condition)
        .sort("publish_time", -1)
        .skip(skip)
        .limit(page_size)
        .to_list(length=None)
    )
    res = list(
        map(
            lambda val: {
                **val,
                **{"_id": str(val["_id"]), "publish_time": str(val["publish_time"])},
            },
            res,
        )
    )
    return res
