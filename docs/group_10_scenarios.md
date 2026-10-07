# Group X — fifteen cases, click by click

**Written 6 October 2026** for the registrar's walk-through of the Group 10 branch
(`claude/group-10-tumor-pathway-3a99f7`). Open **http://localhost:8812**, the server for this
branch. Each line is the exact sequence of options to click, ending with what the tool returns.
The cases are synthetic.

1. **Ovarian dysgerminoma**
   Click: Start guided entry -> Mass / swelling (solid tumour) -> Soft tissue -> Ovary, testis and sacrococcygeal region -> Ovary -> A histology report — biopsy or resection -> Dysgerminoma -> 9060 Dysgerminoma

2. **Ovarian mixed germ cell tumour: dysgerminoma and yolk sac tumour**
   Click: Start guided entry -> Mass / swelling (solid tumour) -> Soft tissue -> Ovary, testis and sacrococcygeal region -> Ovary -> A histology report — biopsy or resection -> Mixed germ cell tumour — more than one germ cell component -> Other combination, or none listed -> 9085 Mixed germ cell tumor

3. **Ovarian immature teratoma, grade 1**
   Click: Start guided entry -> Mass / swelling (solid tumour) -> Soft tissue -> Ovary, testis and sacrococcygeal region -> Ovary -> A histology report — biopsy or resection -> A teratoma, struma ovarii or strumal carcinoid -> Immature teratoma, any grade -> 9080 Teratoma, malignant, NOS

4. **Ovarian mature cystic teratoma**
   Click: Start guided entry -> Mass / swelling (solid tumour) -> Soft tissue -> Ovary, testis and sacrococcygeal region -> Ovary -> A histology report — biopsy or resection -> A teratoma, struma ovarii or strumal carcinoid -> Mature cystic teratoma (mature teratoma) -> No code: 9080/0 Teratoma, benign, outside the group's behaviour

5. **Ovarian juvenile granulosa cell tumour on block review, stains to follow**
   Click: Start guided entry -> Mass / swelling (solid tumour) -> Soft tissue -> Ovary, testis and sacrococcygeal region -> Ovary -> A histology report — biopsy or resection -> A sex cord–stromal tumour — granulosa cell, Sertoli-Leydig cell, Sertoli cell, Leydig cell, steroid cell, thecoma or another -> Juvenile granulosa cell tumour -> No code: 8622/1 Granulosa cell tumor, juvenile, registrar decision required

6. **Gonadoblastoma with an invasive dysgerminoma**
   Click: Start guided entry -> Mass / swelling (solid tumour) -> Soft tissue -> Ovary, testis and sacrococcygeal region -> Ovary -> A histology report — biopsy or resection -> Gonadoblastoma, alone or with another tumour -> Gonadoblastoma with an invasive dysgerminoma -> 9060 Dysgerminoma

7. **Ovarian core biopsy: small round blue cell tumour, stains to follow**
   Click: Start guided entry -> Mass / swelling (solid tumour) -> Soft tissue -> Ovary, testis and sacrococcygeal region -> Ovary -> A histology report — biopsy or resection -> Malignant tumour, type not determined -> Malignant tumour, small cell type -> 8002 Malignant tumor, small cell type

8. **Lymphoma involving the ovary**
   Click: Start guided entry -> Mass / swelling (solid tumour) -> Soft tissue -> Ovary, testis and sacrococcygeal region -> Ovary -> A histology report — biopsy or resection -> Another tumour type — neuroendocrine tumour, lymphoma, leukaemia, sarcoma, a metastatic deposit or another named tumour -> Lymphoma -> Belongs to another group: Group II
   Then: Start new case -> type "Burkitt lymphoma" in the search box -> Burkitt lymphoma -> Group II opens at "What does the lesion look like on the report (one tap)?"

9. **Testicular yolk sac tumour in an infant**
   Click: Start guided entry -> Mass / swelling (solid tumour) -> Soft tissue -> Ovary, testis and sacrococcygeal region -> Descended testis (Scrotal testis) -> A histology report — biopsy or resection -> Yolk sac tumour, prepubertal or postpubertal type (or infantile embryonal carcinoma) -> 9071 Yolk sac tumor, NOS

10. **Testicular embryonal carcinoma with teratoma**
    Click: Start guided entry -> Mass / swelling (solid tumour) -> Soft tissue -> Ovary, testis and sacrococcygeal region -> Descended testis (Scrotal testis) -> A histology report — biopsy or resection -> Mixed germ cell tumour — more than one germ cell component -> Embryonal carcinoma and teratoma only -> 9081 Teratocarcinoma

11. **Paratesticular rhabdomyosarcoma presenting as a testicular mass**
    Click: Start guided entry -> Mass / swelling (solid tumour) -> Soft tissue -> Ovary, testis and sacrococcygeal region -> Descended testis (Scrotal testis) -> A histology report — biopsy or resection -> Another tumour type — neuroendocrine tumour, lymphoma, leukaemia, sarcoma, a metastatic deposit or another named tumour -> Rhabdomyosarcoma or another sarcoma -> Belongs to another group: Group IX
    Then: Start new case -> type "Embryonal rhabdomyosarcoma" in the search box -> Embryonal rhabdomyosarcoma -> Ovary, testis and sacrococcygeal region -> Descended testis (Scrotal testis) -> Stops: "The term and the site point to different groups"

12. **Sacrococcygeal teratoma with a yolk sac tumour, newborn**
    Click: Start guided entry -> Mass / swelling (solid tumour) -> Soft tissue -> Ovary, testis and sacrococcygeal region -> Pelvis, NOS -> Germ Cell, Trophoblastic Tumors and Neoplasms of Gonads -> A histology report — biopsy or resection -> A teratoma or dermoid cyst -> Teratoma with a yolk sac tumour or another malignant germ cell component -> Other combination, or none listed -> 9085 Mixed germ cell tumor

13. **Anterior mediastinal mass, raised alpha-fetoprotein, no tissue**
    Click: Start guided entry -> Mass / swelling (solid tumour) -> Soft tissue -> Mediastinum -> Anterior mediastinum -> Germ Cell, Trophoblastic Tumors and Neoplasms of Gonads -> An imaging report and a serum or cerebrospinal fluid alpha-fetoprotein or human chorionic gonadotropin result — no tissue -> Imaging shows a tumour and the report calls alpha-fetoprotein raised, with or without human chorionic gonadotropin, and the file calls it a germ cell tumour -> 9065 Germ cell tumor, nonseminomatous

14. **Choriocarcinoma of the placenta after a pregnancy**
    Click: Start guided entry -> Mass / swelling (solid tumour) -> Soft tissue -> Uterus and placenta -> Placenta (Fetal membranes) -> A histology report — biopsy or resection -> Choriocarcinoma, gestational or non-gestational -> 9100 Choriocarcinoma, NOS

15. **Germinoma of the pineal gland, normal markers**
    Click: Start guided entry -> Mass / swelling (solid tumour) -> Soft tissue -> Craniopharyngeal duct and pineal gland -> Pineal gland -> Germ Cell, Trophoblastic Tumors and Neoplasms of Gonads -> A histology report — biopsy or resection -> Germinoma -> 9064 Germinoma
    Then: Start new case -> type "Germinoma" in the search box -> Germinoma -> Craniopharyngeal duct and pineal gland -> Pineal gland -> A histology report — biopsy or resection -> Germinoma -> 9064 Germinoma
