document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('factCheckForm');
    const claimInput = document.getElementById('claimInput');
    const checkBtn = document.getElementById('checkBtn');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const resultsSection = document.getElementById('resultsSection');
    const errorSection = document.getElementById('errorSection');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const claim = claimInput.value.trim();
        if (!claim) {
            showError('Please enter a claim to check.');
            return;
        }

        // Show loading state
        showLoading();

        try {
            const response = await fetch('/check', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ claim: claim })
            });

            const data = await response.json();

            if (response.ok) {
                showResults(data);
            } else {
                showError(data.error || 'An error occurred while checking the claim.');
            }
        } catch (error) {
            showError('Network error: Please check your connection and try again.');
        }
    });

    function showLoading() {
        hideAllSections();
        loadingSpinner.style.display = 'block';
        checkBtn.disabled = true;
        checkBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Checking...';
    }

    function hideLoading() {
        loadingSpinner.style.display = 'none';
        checkBtn.disabled = false;
        checkBtn.innerHTML = '<i class="fas fa-search me-2"></i>Check Claim';
    }

    function hideAllSections() {
        resultsSection.style.display = 'none';
        errorSection.style.display = 'none';
        loadingSpinner.style.display = 'none';
    }

    function showResults(data) {
        hideLoading();
        hideAllSections();

        // Update credibility score
        updateCredibilityScore(data.credibility_score);

        // Update AI analysis
        document.getElementById('aiAnalysis').textContent = data.ai_analysis || 'No AI analysis available';

        // Update related articles
        updateRelatedArticles(data.related_articles || []);

        // Update entities
        updateEntities(data.entities || {});

        // Update timestamp
        const timestamp = new Date(data.timestamp).toLocaleString();
        document.getElementById('timestamp').textContent = timestamp;

        resultsSection.style.display = 'block';
    }

    function updateCredibilityScore(score) {
        const credibilityBar = document.getElementById('credibilityBar');
        const credibilityText = document.getElementById('credibilityText');

        credibilityBar.style.width = score + '%';
        credibilityText.textContent = `${score}/100`;

        // Set color based on score
        credibilityBar.className = 'progress-bar';
        if (score >= 70) {
            credibilityBar.classList.add('bg-success');
            credibilityText.textContent += ' - High Credibility';
        } else if (score >= 40) {
            credibilityBar.classList.add('bg-warning');
            credibilityText.textContent += ' - Moderate Credibility';
        } else {
            credibilityBar.classList.add('bg-danger');
            credibilityText.textContent += ' - Low Credibility';
        }
    }

    function updateRelatedArticles(articles) {
        const container = document.getElementById('relatedArticles');
        container.innerHTML = '';

        if (articles.length === 0) {
            container.innerHTML = '<p class="text-muted">No related articles found.</p>';
            return;
        }

        articles.forEach(article => {
            const articleElement = document.createElement('div');
            articleElement.className = 'border rounded p-3 mb-3';
            
            const publishedDate = article.published_at ? 
                new Date(article.published_at).toLocaleDateString() : '';

            articleElement.innerHTML = `
                <h6 class="mb-2">
                    <a href="${article.url}" target="_blank" class="text-decoration-none">
                        ${article.title}
                    </a>
                </h6>
                <p class="text-muted mb-2">${article.description || 'No description available'}</p>
                <small class="text-muted">
                    <strong>Source:</strong> ${article.source}
                    ${publishedDate ? ` • Published: ${publishedDate}` : ''}
                </small>
            `;
            
            container.appendChild(articleElement);
        });
    }

    function updateEntities(entities) {
        const container = document.getElementById('entitiesSection');
        container.innerHTML = '';

        const entityTypes = Object.keys(entities);
        
        if (entityTypes.length === 0) {
            container.innerHTML = '<p class="text-muted">No key entities identified.</p>';
            return;
        }

        entityTypes.forEach(type => {
            if (entities[type].length > 0) {
                const entityGroup = document.createElement('div');
                entityGroup.className = 'mb-2';
                
                const badges = entities[type].map(entity => 
                    `<span class="badge bg-secondary me-1">${entity}</span>`
                ).join('');

                entityGroup.innerHTML = `
                    <strong>${type.charAt(0).toUpperCase() + type.slice(1)}:</strong>
                    <div class="mt-1">${badges}</div>
                `;
                
                container.appendChild(entityGroup);
            }
        });
    }

    function showError(message) {
        hideLoading();
        hideAllSections();
        
        document.getElementById('errorMessage').textContent = message;
        errorSection.style.display = 'block';
    }

    // Auto-resize textarea
    claimInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
});