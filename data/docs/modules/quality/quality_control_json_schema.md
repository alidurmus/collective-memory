# Context7 ERP - Kalite Kontrol Kriterleri JSON Şema Dokümantasyonu

## 🎯 Proje Özeti

Context7 Django ERP sisteminde ürün ve malzemeler için kalite kontrol kriterlerini JSON formatında saklayacak sistem.

## 📋 Mevcut Sistem Analizi

### Current Quality Control Models
```python
# ProductQualityCriterion
- control_type: 'Metric' | 'Visual'
- control_stage: 'In-Process' | 'Final Control' | 'Incoming'
- measurement_name_or_control_point: string
- target_value_or_description: string
- tolerance: string (optional)
- lower_limit: decimal (optional)
- upper_limit: decimal (optional)
- unit: string (optional)
- rank: integer

# MaterialQualityCriterion
- control_type: 'Metric' | 'Visual' | 'Document'
- measurement_name_or_control_point: string
- target_value_or_description: string
- tolerance: string (optional)
- lower_limit: decimal (optional)
- upper_limit: decimal (optional)
- unit: string (optional)
- rank: integer
```

## 🚀 Yeni JSON Şeması Tasarımı

### 1. Ana Kalite Kriterleri JSON Yapısı

```json
{
  "schema_version": "1.0.0",
  "product_id": "integer",
  "material_id": "integer",
  "criteria_type": "product|material",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",
  "criteria_groups": [
    {
      "group_id": "incoming_control",
      "group_name": "Gelen Malzeme Kontrolü",
      "description": "Tedarikçiden gelen malzemelerin kontrol kriterleri",
      "active": true,
      "rank": 1,
      "criteria": [
        {
          "id": "metric_001",
          "type": "metric",
          "name": "Boyutsal Kontrol",
          "description": "Malzeme boyutlarının kontrolü",
          "measurement_method": "caliper",
          "unit": "mm",
          "target_value": 10.0,
          "tolerance": {
            "type": "±",
            "value": 0.1
          },
          "limits": {
            "lower_limit": 9.9,
            "upper_limit": 10.1
          },
          "active": true,
          "rank": 1,
          "metadata": {
            "inspector_required": true,
            "equipment_required": ["caliper", "micrometer"],
            "environment_conditions": {
              "temperature": "20±2°C",
              "humidity": "50±10%"
            }
          }
        },
        {
          "id": "visual_001",
          "type": "visual",
          "name": "Yüzey Kalitesi",
          "description": "Malzeme yüzeyinin görsel kontrolü",
          "evaluation_criteria": [
            {
              "criterion": "çizik",
              "acceptance_level": "minor",
              "max_count": 2,
              "size_limit": "1mm"
            },
            {
              "criterion": "deformasyon",
              "acceptance_level": "none",
              "max_count": 0
            }
          ],
          "visual_aids": [
            {
              "type": "reference_image",
              "url": "/quality/images/surface_ref_001.jpg",
              "description": "Kabul edilebilir yüzey kalitesi örneği"
            }
          ],
          "active": true,
          "rank": 2,
          "metadata": {
            "lighting_required": "500 lux",
            "inspection_angle": "45°",
            "magnification": "2x"
          }
        }
      ]
    },
    {
      "group_id": "in_process_control",
      "group_name": "Süreç İçi Kontrol",
      "description": "Üretim sürecindeki kontrol kriterleri",
      "active": true,
      "rank": 2,
      "criteria": [
        {
          "id": "metric_002",
          "type": "metric",
          "name": "Sıcaklık Kontrolü",
          "description": "İşlem sıcaklığının kontrolü",
          "measurement_method": "thermocouple",
          "unit": "°C",
          "target_value": 200.0,
          "tolerance": {
            "type": "±",
            "value": 5.0
          },
          "limits": {
            "lower_limit": 195.0,
            "upper_limit": 205.0
          },
          "active": true,
          "rank": 1,
          "metadata": {
            "measurement_frequency": "every_30_minutes",
            "calibration_required": true,
            "calibration_interval": "3_months"
          }
        }
      ]
    },
    {
      "group_id": "final_control",
      "group_name": "Son Kontrol",
      "description": "Bitmiş ürün kontrol kriterleri",
      "active": true,
      "rank": 3,
      "criteria": [
        {
          "id": "functional_001",
          "type": "functional",
          "name": "Fonksiyonel Test",
          "description": "Ürün fonksiyonelliğinin testi",
          "test_procedure": {
            "steps": [
              {
                "step": 1,
                "description": "Cihazı açma testi",
                "expected_result": "LED yeşil yanmalı",
                "duration": "5 seconds"
              },
              {
                "step": 2,
                "description": "Kalibrasyon testi",
                "expected_result": "±0.1% hassasiyet",
                "duration": "30 seconds"
              }
            ]
          },
          "acceptance_criteria": {
            "all_steps_pass": true,
            "max_retry_count": 3
          },
          "active": true,
          "rank": 1,
          "metadata": {
            "test_environment": "controlled_conditions",
            "documentation_required": true
          }
        }
      ]
    }
  ]
}
```

### 2. Kriter Türleri (Criterion Types)

#### 2.1 Metrik Kriterler (Metric Criteria)
```json
{
  "type": "metric",
  "measurement_method": "caliper|micrometer|scale|gauge|thermocouple|pressure_gauge",
  "unit": "mm|cm|m|g|kg|°C|bar|psi|V|A|Hz",
  "target_value": "number",
  "tolerance": {
    "type": "±|+/-|%|range",
    "value": "number",
    "percentage": "number"
  },
  "limits": {
    "lower_limit": "number",
    "upper_limit": "number",
    "control_limits": {
      "ucl": "number",
      "lcl": "number"
    }
  },
  "measurement_conditions": {
    "temperature": "string",
    "humidity": "string",
    "pressure": "string"
  }
}
```

#### 2.2 Görsel Kriterler (Visual Criteria)
```json
{
  "type": "visual",
  "evaluation_criteria": [
    {
      "criterion": "scratch|dent|discoloration|crack|void",
      "acceptance_level": "none|minor|major|critical",
      "max_count": "integer",
      "size_limit": "string",
      "location_restriction": "string"
    }
  ],
  "visual_aids": [
    {
      "type": "reference_image|color_chart|texture_sample",
      "url": "string",
      "description": "string"
    }
  ],
  "inspection_conditions": {
    "lighting": "string",
    "angle": "string",
    "magnification": "string",
    "background": "string"
  }
}
```

#### 2.3 Fonksiyonel Kriterler (Functional Criteria)
```json
{
  "type": "functional",
  "test_procedure": {
    "steps": [
      {
        "step": "integer",
        "description": "string",
        "expected_result": "string",
        "duration": "string",
        "tools_required": ["string"]
      }
    ]
  },
  "acceptance_criteria": {
    "all_steps_pass": "boolean",
    "pass_percentage": "number",
    "max_retry_count": "integer"
  },
  "test_environment": {
    "conditions": "string",
    "equipment": ["string"]
  }
}
```

#### 2.4 Dokümantasyon Kriterler (Documentation Criteria)
```json
{
  "type": "documentation",
  "required_documents": [
    {
      "document_type": "certificate|spec_sheet|test_report|drawing",
      "document_name": "string",
      "version_required": "string",
      "validity_period": "string"
    }
  ],
  "verification_method": "visual_check|digital_signature|stamp",
  "compliance_standards": ["ISO_9001", "CE", "FDA"]
}
```

### 3. Veri Doğrulama Kuralları (Validation Rules)

```json
{
  "validation_rules": {
    "mandatory_fields": ["id", "type", "name", "description"],
    "type_specific_required": {
      "metric": ["unit", "target_value", "limits"],
      "visual": ["evaluation_criteria"],
      "functional": ["test_procedure", "acceptance_criteria"],
      "documentation": ["required_documents"]
    },
    "data_constraints": {
      "id": "^[a-z]+_[0-9]{3}$",
      "rank": "1-999",
      "target_value": "number",
      "limits": "lower_limit < upper_limit"
    }
  }
}
```

### 4. Kalite Kontrol Formu JSON Yapısı

```json
{
  "form_id": "incoming_001",
  "form_type": "incoming|in_process|final",
  "date": "2024-01-01",
  "inspector": {
    "id": "integer",
    "name": "string",
    "certification": "string"
  },
  "item": {
    "code": "string",
    "description": "string",
    "batch_number": "string",
    "quantity": "integer"
  },
  "evaluation_results": [
    {
      "criterion_id": "metric_001",
      "measured_value": 10.05,
      "result": "pass|fail|conditional",
      "notes": "string",
      "measurement_data": {
        "readings": [10.04, 10.05, 10.06],
        "average": 10.05,
        "deviation": 0.01
      }
    },
    {
      "criterion_id": "visual_001",
      "evaluation_results": [
        {
          "criterion": "çizik",
          "count": 1,
          "size": "0.5mm",
          "result": "pass"
        }
      ],
      "overall_result": "pass",
      "notes": "Kabul edilebilir düzeyde"
    }
  ],
  "overall_status": "approved|rejected|conditional",
  "comments": "string",
  "attachments": [
    {
      "type": "photo|document|measurement_data",
      "url": "string",
      "description": "string"
    }
  ]
}
```

### 5. Avantajlar ve Özellikler

#### 5.1 Esneklik
- Dinamik kriter ekleme/çıkarma
- Farklı ölçüm yöntemleri
- Çoklu tolerans tanımları
- Koşullu kriterler

#### 5.2 Genişletilebilirlik
- Yeni kriter türleri eklenebilir
- Metadata ile ek bilgiler
- Entegrasyon desteği
- Versiyonlama sistemi

#### 5.3 Veri Bütünlüğü
- JSON şema validasyonu
- Referans bütünlüğü
- Audit trail
- Backup desteği

### 6. Implementation Notları

1. **Django JSONField** kullanarak esnek veri saklama
2. **Pydantic models** ile veri validasyonu
3. **DRF serializers** ile API entegrasyonu
4. **Context7 Glassmorphism** ile modern UI
5. **Real-time validation** ile kullanıcı deneyimi

### 7. Migration Stratejisi

```python
# Mevcut ProductQualityCriterion -> JSON dönüşümü
def migrate_existing_criteria():
    for criterion in ProductQualityCriterion.objects.all():
        json_data = {
            "schema_version": "1.0.0",
            "criteria_groups": [{
                "group_id": criterion.control_stage.lower().replace(" ", "_"),
                "criteria": [{
                    "id": f"{criterion.control_type.lower()}_{criterion.id}",
                    "type": criterion.control_type.lower(),
                    "name": criterion.measurement_name_or_control_point,
                    "description": criterion.target_value_or_description,
                    "unit": criterion.unit,
                    "target_value": criterion.target_value_or_description,
                    "limits": {
                        "lower_limit": criterion.lower_limit,
                        "upper_limit": criterion.upper_limit
                    },
                    "tolerance": criterion.tolerance,
                    "rank": criterion.rank
                }]
            }]
        }
        # Yeni JSON tabanlı modele kaydet
```

## 🔗 Entegrasyon Noktaları

1. **Quality Control Forms** - Mevcut formlar ile entegrasyon
2. **Product/Material Models** - Ana veri modelleri ile ilişki
3. **User Management** - Inspector yetkilendirmesi
4. **Reporting System** - Kalite raporları
5. **API Endpoints** - Mobil ve harici sistem entegrasyonu

## 📊 Performans Optimizasyonu

- **Indexing**: JSON alanları için GIN indexleri
- **Caching**: Frequently accessed criteria için Redis
- **Lazy Loading**: Büyük JSON veriler için
- **Compression**: Büyük attachment'lar için

## 🔒 Güvenlik Önlemleri

- **Input Validation**: JSON şema validasyonu
- **Access Control**: Rol tabanlı yetkilendirme
- **Audit Trail**: Tüm değişikliklerin kaydı
- **Backup**: Düzenli yedekleme sistemi 