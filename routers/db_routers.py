class CachDatabase:
    def db_for_read(self, model, **hints):
        if model.__meta.app_label == 'items':
            return 'products_cache'
        return None

    def db_for_write(self, model, **hints):
        if model.__meta.app_label:
            return 'products_cache'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'products_cache':
            return db == 'products_cache'
        return None
