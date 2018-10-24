from import_export import resources
from .models import BankStatement


class BankStatementResource(resources.ModelResource):
    class Meta:
        model = BankStatement
        import_date_field = 'date'
        import_amount_field = 'amount'
        import_description_field = 'description'

        # import_id_fields = ('vendor_code',)

        fields = ('id', 'date', 'post',
                  'description', 'amount', 'category',
                  'bank_name', 'owner', 'statement_source')
        # exclude = ('post_date',)

        skip_unchanged = True
        report_skipped = False
        dry_run = True

    def skip_row(self, instance, original):
        # print('hello')
        # original_id_value = getattr(original, self._meta.import_date_field) + \
        #                     getattr(original, self._meta.import_amount_field) + \
        #                     getattr(original, self._meta.import_description_field)
        #
        # instance_id_value = getattr(instance, self._meta.import_date_field) + \
        #                     getattr(instance, self._meta.import_amount_field) + \
        #                     getattr(instance, self._meta.import_description_field)
        #
        # if original_id_value != instance_id_value:
        #     return True
        if not self._meta.skip_unchanged:
            return False

        fields = self.get_fields()
        for field in self.get_fields():
            try:
                if list(field.get_value(instance).all()) != list(field.get_value(original).all()):
                    return False
            except AttributeError:
                if field.get_value(instance) != field.get_value(original):
                    return False
        return True