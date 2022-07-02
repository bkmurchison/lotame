from lotame.api import Api


class AudienceService(object):
    """
    # AudienceService Class
    #   Provides helper methods for the Lotame API audience service
    """
    # statics
    AUDIENCE_SERVICE = "/audiences"

    def __init__(self, api=None):
        if api is None:
            api = Api()
        self.api = api

    def get(self, audience=""):
        url = self.api.build_url(
            self.AUDIENCE_SERVICE + "/" + str(audience), {}, False)
        audience = self.api.get(url)
        return audience

    def getList(self, params={}):
        url = self.api.build_url(self.AUDIENCE_SERVICE, params)
        audience_list = self.api.get(url)
        return audience_list

    def get_create_audience_json(
            self, audience_name, client_id, behavior_groups, description='',
            condition_between_grouops='OR', condition_within_group='AND',
            **custom_request_params):
        """Constructs minimal json audience definition.

        behavior_groups (list): list of behavior ids.
            For example: [[244, 343, 345], [33, 235]]
            Where there is AND condition between ids in the sub list, and
            OR condition on the groups of sub lists, that is:
            [[244 AND 343 AND 345] OR [33 AND 235]]

        Args:
            audience_name (str): audience name.
            client_id (int): id of client this audience should belong to.
            behavior_groups (list): 2 dimensional list of behavior ids.
            description (str[optional]): description of this audience.
            condition_between_grouops (str[optional]): condition between groups of behaviors.
            condition_within_group (str[optional]): condition within each group of behaviors.
            custom_request_params (dict): custom request params.
        Returns:
            dict: audience definition:
                {
                  'name': audience_name,
                  'clientId': client_id,
                  'definition': ....,
                  'description': '.......'
                }
        """
        component = []
        for index, behavior_group in enumerate(behavior_groups):
            tmp = {
                'operator': None
            }
            if len(behavior_group) == 1:
                tmp['complexAudienceBehavior'] = {
                    'purchased': True,
                    'behavior': {
                        'id': behavior_group[0]
                    },
                }
            else:
                tmp['component'] = []
                for index2, behavior in enumerate(behavior_group):
                    tmp2 = {
                        'operator': None,
                        'complexAudienceBehavior': {
                            'purchased': True,
                            'behavior': {
                                'id': behavior
                            }
                        }
                    }
                    if index2 != 0:
                        tmp2['operator'] = condition_within_group
                    tmp['component'].append(tmp2)
            if index != 0:
                tmp['operator'] = condition_between_grouops
            component.append(tmp)

        definition = {
            'name': audience_name,
            'clientId': client_id,
            'definition': {'component': component}
        }
        if len(custom_request_params.items()) > 0:
            for k, v in custom_request_params.items():
                if k not in ['name', 'clientId', 'definition']:
                    definition[k] = v
        if 'overlap' not in definition:
            definition['overlap'] = True

        if description:
            definition['description'] = description
        return definition
