import falcon
from pony.orm import db_session, desc
from models.schema import TransaksiBelanja
from datetime import datetime


class LaporanBelanjaResource:
    @db_session
    def on_get(self, req, resp):
        start = req.get_param('start')
        end = req.get_param('end')

        try:
            query = TransaksiBelanja.select()

            if start:
                start_date = datetime.strptime(start, "%Y-%m-%d")
                query = query.filter(
                    lambda x: x.tanggal >= start_date
                )

            if end:
                end_date = datetime.strptime(end, "%Y-%m-%d")
                query = query.filter(
                    lambda x: x.tanggal <= end_date
                )

            data = []
            total = 0

            for b in query.order_by(lambda x: desc(x.id)):
                total += float(b.nominal or 0)

                data.append({
                    "id": b.id,
                    "tanggal": b.tanggal.strftime("%Y-%m-%d"),
                    "keterangan": b.keterangan or "-",
                    "nominal": float(b.nominal or 0)
                })

            resp.media = {
                "status": "success",
                "total_belanja": total,
                "data": data
            }

        except Exception as e:
            import traceback
            print(traceback.format_exc())

            resp.status = falcon.HTTP_500
            resp.media = {
                "status": "error",
                "message": str(e)
            }