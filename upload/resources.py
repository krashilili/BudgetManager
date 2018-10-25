from import_export import resources
from .models import BankStatement


class BankStatementResource(resources.ModelResource):
    class Meta:
        model = BankStatement
        import_id_fields = ('slug',)
        import_amount_field = 'amount'
        import_description_field = 'description'

        # import_id_fields = ('vendor_code',)

        fields = ('date', 'post',
                  'description', 'amount', 'category',
                  'bank_name', 'owner', 'statement_source', 'slug',)
        # exclude = ('post_date',)

        skip_unchanged = True
        report_skipped = True
        # dry_run = True

    def get_instance(self, instance_loader, row):
        try:
            params = {}
            for key in instance_loader.resource.get_import_id_fields():
                field = instance_loader.resource.fields[key]
                params[field.attribute] = field.clean(row)
            return self.get_queryset().get(**params)
        except Exception:
            pass

