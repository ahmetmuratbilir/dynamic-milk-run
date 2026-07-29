"""
data_loader.py
==============
Veri Soyutlama Katmani (Data Abstraction Layer)

Bu modül, data/config.json dosyasındaki "data_source" ayarına göre ('synthetic' veya 'real')
verileri dinamik olarak okur. Sistem kodlarının geri kalanı (simülasyon, optimizasyon, arayüz)
verinin nereden geldiğini bilmek zorunda kalmaz.

Kullanım:
    from src.data_loader import DataLoader
    loader = DataLoader()
    stations_df = loader.get_stations()
    consumption_df = loader.get_consumption()
"""

import os
import json
import pandas as pd

class DataLoader:
    def __init__(self, config_path=None):
        if config_path is None:
            # Proje kok dizinine gore config.json yolunu belirle
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, "data", "config.json")
        
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = config_path
        self.config = self._load_config()
        self.data_source = self.config.get("data_source", "synthetic")
        self.data_dir = os.path.join(self.base_dir, "data", self.data_source)

    def _load_config(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config dosyasi bulunamadi: {self.config_path}")
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_source_type(self):
        """Aktif veri kaynagi turunu doner ('synthetic' veya 'real')."""
        return self.data_source

    def get_stations(self) -> pd.DataFrame:
        """Istasyon tanim bilgilerini yukler."""
        path = os.path.join(self.data_dir, "stations.csv")
        return pd.read_csv(path, encoding="utf-8")

    def get_consumption(self) -> pd.DataFrame:
        """Dakikalik stokastik tuketim verisini yukler."""
        path = os.path.join(self.data_dir, "consumption.csv")
        return pd.read_csv(path, encoding="utf-8")

    def get_inventory(self) -> pd.DataFrame:
        """Baslangic stok ve Kanban ayarlarini yukler."""
        path = os.path.join(self.data_dir, "inventory.csv")
        return pd.read_csv(path, encoding="utf-8")

    def get_vehicles(self) -> pd.DataFrame:
        """Milk-run arac parametrelerini yukler."""
        path = os.path.join(self.data_dir, "vehicles.csv")
        return pd.read_csv(path, encoding="utf-8")

    def get_distances(self) -> pd.DataFrame:
        """Nodes (Depo + Istasyonlar) arasi mesafe ve sure matrisini yukler."""
        path = os.path.join(self.data_dir, "distances.csv")
        return pd.read_csv(path, encoding="utf-8")

    def get_production_plan(self) -> pd.DataFrame:
        """Uretim plan verisini yukler."""
        path = os.path.join(self.data_dir, "production_plan.csv")
        return pd.read_csv(path, encoding="utf-8")


if __name__ == "__main__":
    # DataLoader testi
    loader = DataLoader()
    print(f"Aktif Veri Kaynagi: {loader.get_source_type()}")
    st_df = loader.get_stations()
    print(f"Istasyon Sayisi: {len(st_df)}")
    cons_df = loader.get_consumption()
    print(f"Tuketim Veri Satiri: {len(cons_df)}")
    print("DataLoader testi basariyla tamamlandi!")
