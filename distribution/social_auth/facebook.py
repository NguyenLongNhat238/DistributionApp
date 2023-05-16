import facebook


class Facebook:
    """
    Facebook class to fetch the user info and return it
    """

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the facebook GraphAPI to fetch the user info
        """
        try:
            graph = facebook.GraphAPI(access_token=auth_token)
            # profile = graph.request('/me?fields=name,email')

            profile = graph.get_object('me')
            args = {'fields': 'id,name,email,picture', }
            profile = graph.get_object('me', **args)
            return profile
        except:
            return "The token is invalid or expired."
