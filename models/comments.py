class Comments():
    def __init__(self, id, post_id, author_id, content, created_on):
        self.id = id
        self.post_id = None
        self.author_id = author_id
        self.content = content
        self.created_on = created_on