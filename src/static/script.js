document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('impactForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const submitBtn = document.getElementById('submitBtn');
        const resultDiv = document.getElementById('result');
        
        // Disable button and show loading
        submitBtn.disabled = true;
        submitBtn.textContent = 'Analizando...';
        resultDiv.style.display = 'block';
        resultDiv.value = 'Analizando iniciativa, por favor espere...';
        
        // Clear previous errors
        const existingError = document.querySelector('.error');
        if (existingError) {
            existingError.remove();
        }
        
        // Get form data
        const formData = {
            initiative_name: document.getElementById('initiative_name').value,
            initial_investment: parseFloat(document.getElementById('initial_investment').value),
            business_objective: document.getElementById('business_objective').value,
            expected_impact: parseFloat(document.getElementById('expected_impact').value)
        };
        
        try {
            const response = await fetch('/impact-analysis', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error en la solicitud');
            }
            
            const result = await response.text();
            resultDiv.value = result;
            
        } catch (error) {
            console.error('Error:', error);
            resultDiv.value = '';
            resultDiv.style.display = 'none';
            
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error';
            errorDiv.textContent = 'Error: ' + error.message;
            document.querySelector('.container').appendChild(errorDiv);
        } finally {
            // Re-enable button
            submitBtn.disabled = false;
            submitBtn.textContent = 'Analizar Impacto';
        }
    });
}); 