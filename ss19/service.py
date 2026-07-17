from sqlalchemy.orm import Session
from fastapi import HTTPException

import models, schemas


def create_warehouse(db: Session, warehouse_in: schemas.WarehouseCreate):
    new_warehouse = models.Warehouse(**warehouse_in.model_dump())
    try:
        db.add(new_warehouse)
        db.commit()
        db.refresh(new_warehouse)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Lỗi khi tạo nhà kho")
    return new_warehouse


def get_warehouse_detail(db: Session, warehouse_id: int):
    warehouse = db.query(models.Warehouse).filter(models.Warehouse.id == warehouse_id).first()
    if not warehouse:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhà kho")
    return warehouse


def update_package(db: Session, package_id: int, package_in: schemas.PackageUpdate):
    package = db.query(models.Package).filter(models.Package.id == package_id).first()
    if not package:
        raise HTTPException(status_code=404, detail="Không tìm thấy kiện hàng")

    update_data = package_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(package, field, value)

    try:
        db.commit()
        db.refresh(package)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Lỗi khi cập nhật kiện hàng")
    return package


def delete_waybill(db: Session, waybill_id: int):
    waybill = db.query(models.Waybill).filter(models.Waybill.id == waybill_id).first()
    if not waybill:
        raise HTTPException(status_code=404, detail="Không tìm thấy vận đơn")

    try:
        db.delete(waybill)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Lỗi khi xóa vận đơn")