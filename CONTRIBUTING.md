# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir al Survey Analytics Dashboard!

---

## 🍴 Cómo contribuir

### 1. Fork el repositorio

Haz clic en "Fork" en GitHub para crear tu propia copia del proyecto.

### 2. Clona tu fork

```bash
git clone https://github.com/TU-USUARIO/survey-analytics-dashboard.git
cd survey-analytics-dashboard
```

### 3. Crea una rama

```bash
git checkout -b feature/tu-nueva-funcionalidad
```

### 4. Realiza tus cambios

- Sigue el estilo de código existente
- Comenta tu código
- Prueba tus cambios

### 5. Commit

```bash
git add .
git commit -m "Añadir: descripción clara de tu cambio"
```

### 6. Push

```bash
git push origin feature/tu-nueva-funcionalidad
```

### 7. Pull Request

Ve a GitHub y crea un Pull Request describiendo tus cambios.

---

## 📐 Estándares de Código

### Python

- Sigue [PEP 8](https://pep8.org/)
- Usa type hints
- Documenta funciones y clases
- Nombres descriptivos en inglés o español (consistente)

```python
def load_from_path(self, path: str | Path) -> list[SurveyResponse]:
    """Carga CSV desde el sistema de archivos."""
    ...
```

### JavaScript

- Usa ES6+
- Funciones flecha cuando sea posible
- Nombres en camelCase

```javascript
const handleAnalyze = async (event) => {
    // Código aquí
};
```

### CSS

- Usa variables CSS
- Sigue la metodología BEM (opcional)
- Mobile-first

---

## 🧪 Testing

Antes de enviar un PR:

```bash
# Probar endpoints
curl http://localhost:8000/api/survey/stats

# Probar análisis IA
curl -X POST http://localhost:8000/api/ai/analyze \
  -H "Content-Type: application/json" \
  -d '{"column_key": "comments"}'
```

---

## 📝 Convenciones de Commit

Usa [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Formato, sin cambios de lógica
- `refactor:` Refactorización
- `test:` Tests
- `chore:` Mantenimiento

Ejemplos:

```bash
feat: agregar filtro por fecha en dashboard
fix: corregir error de conexión con Google Sheets
docs: actualizar README con instrucciones de Groq
refactor: optimizar carga de datos en data_loader.py
```

---

## 🐛 Reportar Bugs

Usa GitHub Issues e incluye:

- Descripción clara del problema
- Pasos para reproducir
- Comportamiento esperado
- Comportamiento actual
- Versión del proyecto
- Sistema operativo
- Logs de error (si aplica)

---

## 💡 Sugerencias

¡Las sugerencias son bienvenidas! Crea un issue con la etiqueta `enhancement` y describe:

- Qué te gustaría ver
- Por qué sería útil
- Cómo podría implementarse (opcional)

---

## 📄 Licencia

Al contribuir, aceptas que tu código se distribuya bajo la [Licencia MIT](LICENSE).

---

## 🙏 Reconocimientos

Todos los contribuyentes serán listados en el README principal.

---

**¡Gracias por hacer este proyecto mejor!** 🎉
