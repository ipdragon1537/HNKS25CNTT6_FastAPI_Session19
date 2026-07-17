from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models, schemas, service
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Supply Chain API")


@app.post("/warehouses", response_model=schemas.WarehouseResponse, status_code=201)
def create_warehouse(warehouse_in: schemas.WarehouseCreate, db: Session = Depends(get_db)):
    return service.create_warehouse(db, warehouse_in)


@app.get("/warehouses/{warehouse_id}", response_model=schemas.WarehouseDetailResponse)
def get_warehouse_detail(warehouse_id: int, db: Session = Depends(get_db)):
    return service.get_warehouse_detail(db, warehouse_id)


@app.patch("/packages/{package_id}", response_model=schemas.PackageResponse)
def update_package(package_id: int, package_in: schemas.PackageUpdate, db: Session = Depends(get_db)):
    return service.update_package(db, package_id, package_in)


@app.delete("/waybills/{waybill_id}")
def delete_waybill(waybill_id: int, db: Session = Depends(get_db)):
    service.delete_waybill(db, waybill_id)
    return {"message": "Đã xóa vận đơn"}
@app.post("/packages", response_model=schemas.PackageResponse, status_code=201)
def create_package(package_in: schemas.PackageCreate, db: Session = Depends(get_db)):
    new_package = models.Package(**package_in.model_dump())
    db.add(new_package)
    db.commit()
    db.refresh(new_package)
    return new_package
@app.post("/waybills", response_model=schemas.WaybillResponse, status_code=201)
def create_waybill(waybill_in: schemas.WaybillCreate, db: Session = Depends(get_db)):
    new_waybill = models.Waybill(**waybill_in.model_dump())
    db.add(new_waybill)
    db.commit()
    db.refresh(new_waybill)
    return new_waybill