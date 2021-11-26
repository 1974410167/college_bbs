import django.db.models.query_utils
from django.apps import apps

from user.models import UserProfile


class DataFetch:

    def __init__(self, objs, configs):
        self.objs = objs
        self.configs = configs

        if not isinstance(self.objs, list):
            self.objs = [self.objs]

        for key, val in configs.items():
            self.foreign_id = key
            self.foreign_model = val[0]
            self.fields = val[1]

            if not self.objs:
                raise ValueError("objs must not empty")
            if not self.objs[0].get(self.foreign_id, None):
                raise KeyError(f"objs has not {self.foreign_id} attribute")

            foreign_ids = []
            for obj in self.objs:
                fign_id = obj.get(self.foreign_id)
                foreign_ids.append(fign_id)

            objects = getattr(self.foreign_model, "objects")
            self.fields.append("id")
            q = objects.filter(id__in=foreign_ids).values(*self.fields)
            data = {}
            for data_obj in q:
                data_obj_id = data_obj["id"]
                data[data_obj_id] = data_obj

            if len(val) > 2:
                for obj1 in self.objs:
                    id1 = obj1.get(self.foreign_id)
                    obj1[val[2]] = data.get(id1)
            else:
                for obj1 in self.objs:
                    id1 = obj1.get(self.foreign_id)
                    field = self.foreign_id.split("_")[0]
                    obj1[field] = data.get(id1)
