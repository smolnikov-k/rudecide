---
language:
  - ru
license: other
license_name: mixed-open
pretty_name: RuDecide
size_categories:
  - 1K<n<10K
task_categories:
  - text-classification
  - multiple-choice
tags:
  - typed-decisions
  - system-one
  - russian
  - benchmark
  - agents
configs:
  - config_name: track_a_unseen
    data_files: data/track_a_unseen.jsonl
  - config_name: track_b_applied
    data_files: data/track_b_applied.jsonl
---

# RuDecide v0.1

Русский бенчмарк для маленьких моделей «быстрых решений» (класс System One: Jev, Laya, JevK5, decider, Kev).
Модель получает ситуацию (`state`) и типизированный вопрос: выбор варианта (`choice`), порядковая шкала (`score`)
или «да/нет» (`noul`), и должна вернуть распределение вероятностей по вариантам. Текст модель не генерирует.

A Russian benchmark for small typed-decision ("System One") models. Each item is a `state` plus one typed question
(`choice` / `score` / `noul`); the model returns a probability distribution over the options.

## Треки

| Трек | Что проверяет | Вопросов |
|---|---|---|
| `track_a_unseen` | Русские задачи с человеческой разметкой: понимание текста, логический вывод, здравый смысл, эмоции. Для честного сравнения моделей, которые эти задачи не учили. | 2 235 |
| `track_b_applied` | Прикладные задачи ИИ-агентов на русском: разбор обращений в поддержку, атаки на ассистента, намерения пользователя, спам, выбор навыка из незнакомого каталога с вариантом «навык не нужен». | 1 543 |

### Задачи трека A

| task | тип | вариантов | источник (лицензия) |
|---|---|---|---|
| danetqa | noul | 2 | DaNetQA, Russian SuperGLUE val (MIT) |
| muserc | noul | 2 | MuSeRC, Russian SuperGLUE val (MIT) |
| parus | choice | 2 | PARus, Russian SuperGLUE val (MIT) |
| rcb | choice | 3 | RCB, Russian SuperGLUE val (MIT) |
| rucola | noul | 2 | RuCoLA dev (Apache-2.0) |
| xstory_ru | choice | 2 | xStoryCloze ru eval (CC BY-SA 4.0) |
| ruopenbookqa | choice | 4 | MERA ruOpenBookQA train (MIT) |
| ruworldtree | choice | 4 | MERA ruWorldTree train (MIT) |
| cedr | choice | 6 | CEDR, ai-forever test (Apache-2.0), только однометочные |

### Задачи трека B

| task | тип | источник (лицензия) |
|---|---|---|
| support_ru | choice / score / noul | A11Sunday/support-json-ru test (CC BY 4.0) |
| injection_ru | noul | dmtrdr/russian_prompt_injections (Apache-2.0) против бенигнов MASSIVE ru |
| prompt_safety | choice | Nailyk14/prompt-safety-multilingual test, русские строки с Apache/MIT |
| massive_ru | choice | MASSIVE ru test (CC BY 4.0): область запроса и действие |
| spam_ru | noul | DmitryKRX/anti_spam_ru (Apache-2.0) |
| skills_unseen_catalogs | choice | синтетика: 6 каталогов навыков выдуманных ассистентов, сообщения сгенерированы открытой моделью DeepSeek (MIT); каталоги не пересекаются с обучающими |

Официальные тестовые метки Russian SuperGLUE и MERA закрыты, поэтому используются размеченные val/dev/train части.
В каждой задаче не больше 300 вопросов.

## Формат

```json
{"id": "track_a_unseen-danetqa-00000", "track": "track_a_unseen", "task": "danetqa",
 "state": "Текст: ...",
 "question": {"type": "noul", "instructions": "Ответ на вопрос «...» - да?", "criteria": null},
 "answer": "true"}
```

`answer`: для `choice` - ключ из `criteria`; для `noul` - `"true"`/`"false"`; для `score` - индекс уровня строкой.
Формат совместим с запросом `/v1/systemone` (TypeSafe Jev API).

## Как посчитать

Сохраните ответы модели в `predictions.jsonl`, по строке на вопрос: `{"id": ..., "probabilities": {"вариант": p, ...}}`
(или `{"id": ..., "prediction": "вариант"}`), и запустите:

```bash
python score.py data/track_a_unseen.jsonl predictions.jsonl
```

## Метрики

- `acc` - доля верных (argmax распределения совпал с ответом), по каждой задаче.
- `skill` - точность сверх угадывания: `(acc - 1/K) / (1 - 1/K)`, K - число вариантов; среднее по задачам трека.
- Рекомендуем также ECE (калибровку вероятностей).

## Результаты v0.1 (без дообучения на этих задачах, если не сказано иное)

| Модель | Трек A acc / skill | Трек B acc / skill |
|---|---|---|
| decider-2b v11 (Mapika) | 78,6 / 65,4 | 75,7 / 62,1 |
| JevK5-2B v0.2 | 70,8 / 51,8 | 69,4 / 51,1 |
| Кивок 0.3B* | 51,4 / 18,9 | 91,1 / 88,0 |
| Laya-multilingual 322M | 48,9 / 14,8 | 53,6 / 35,6 |

\* Кивок обучен на тренировочных частях источников трека B (кроме каталогов навыков), поэтому его результат на треке B
показывает эффект дообучения, а не обобщение. Трек A он не видел.

## Лицензия

Сборка распространяется на условиях лицензий источников (MIT, Apache-2.0, CC BY 4.0, CC BY-SA 4.0 для xstory_ru).
Задача `xstory_ru` наследует CC BY-SA 4.0. Синтетические данные трека B - CC BY 4.0.
Пожалуйста, не обучайте модели на этом наборе, иначе сравнение теряет смысл.

## Цитирование

Smolnikov / CapyAgent, RuDecide v0.1, 2026.
