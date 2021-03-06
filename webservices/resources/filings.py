from flask.ext.restful import Resource

from webservices import args
from webservices import docs
from webservices import spec
from webservices import utils
from webservices import schemas
from webservices.common import models
from webservices.common.util import filter_query


fields = {
    'committee_id',
    'beginning_image_number',
    'report_type',
    'report_year',
    'recipt_date',
    'form_type',
    'primary_general_indicator',
    'amendment_indicator',
}

range_fields = [
    (('min_receipt_date', 'max_receipt_date'), models.Filings.receipt_date),
]


@spec.doc(
    tags=['filings'],
    description=docs.FILINGS,
    path_params=[
        {
            'name': 'committee_id',
            'in': 'path',
            'description': docs.COMMITTEE_ID,
            'type': 'string',
        },
    ],
)
class FilingsView(Resource):

    @args.register_kwargs(args.paging)
    @args.register_kwargs(
        args.make_sort_args(
            default=['-receipt_date'],
            validator=args.IndexValidator(models.Filings),
        )
    )
    @schemas.marshal_with(schemas.FilingsPageSchema())
    def get(self, committee_id=None, **kwargs):
        filings = models.Filings.query
        filings = filings.filter_by(committee_id=committee_id)
        return utils.fetch_page(filings, kwargs, model=models.Filings)


@spec.doc(
    tags=['filings'],
    description=docs.FILINGS,
)
class FilingsList(Resource):

    @args.register_kwargs(args.paging)
    @args.register_kwargs(args.filings)
    @args.register_kwargs(
        args.make_sort_args(
            default=['-receipt_date'],
            validator=args.IndexValidator(models.Filings),
        )
    )
    @schemas.marshal_with(schemas.FilingsPageSchema())
    def get(self, **kwargs):
        query = models.Filings.query
        query = filter_query(models.Filings, query, fields, kwargs)
        query = utils.filter_range(query, kwargs, range_fields)
        return utils.fetch_page(query, kwargs, model=models.Filings)
