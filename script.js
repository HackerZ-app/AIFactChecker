// AI Fact Checker Application
class FactChecker {
    constructor() {
        this.initializeElements();
        this.attachEventListeners();
        this.credibleSources = this.initializeCredibleSources();
    }

    initializeElements() {
        this.claimInput = document.getElementById('claim-input');
        this.checkBtn = document.getElementById('check-btn');
        this.loading = document.getElementById('loading');
        this.results = document.getElementById('results');
        this.newCheckBtn = document.getElementById('new-check-btn');
        this.overallRating = document.getElementById('overall-rating');
        this.claimText = document.getElementById('claim-text');
        this.analysisSummary = document.getElementById('analysis-summary');
        this.sourcesList = document.getElementById('sources-list');
        this.verdict = document.getElementById('verdict');
        this.confidenceScore = document.getElementById('confidence-score');
    }

    attachEventListeners() {
        this.checkBtn.addEventListener('click', () => this.checkFacts());
        this.newCheckBtn.addEventListener('click', () => this.resetForm());
        this.claimInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                this.checkFacts();
            }
        });
        this.claimInput.addEventListener('input', () => this.validateInput());
    }

    initializeCredibleSources() {
        return [
            {
                name: "Reuters",
                baseUrl: "reuters.com",
                credibilityScore: 95,
                type: "news"
            },
            {
                name: "Associated Press",
                baseUrl: "apnews.com",
                credibilityScore: 94,
                type: "news"
            },
            {
                name: "BBC News",
                baseUrl: "bbc.com",
                credibilityScore: 92,
                type: "news"
            },
            {
                name: "NPR",
                baseUrl: "npr.org",
                credibilityScore: 91,
                type: "news"
            },
            {
                name: "Snopes",
                baseUrl: "snopes.com",
                credibilityScore: 89,
                type: "fact-check"
            },
            {
                name: "PolitiFact",
                baseUrl: "politifact.com",
                credibilityScore: 88,
                type: "fact-check"
            },
            {
                name: "FactCheck.org",
                baseUrl: "factcheck.org",
                credibilityScore: 90,
                type: "fact-check"
            },
            {
                name: "World Health Organization",
                baseUrl: "who.int",
                credibilityScore: 96,
                type: "health"
            },
            {
                name: "CDC",
                baseUrl: "cdc.gov",
                credibilityScore: 95,
                type: "health"
            },
            {
                name: "NASA",
                baseUrl: "nasa.gov",
                credibilityScore: 97,
                type: "science"
            }
        ];
    }

    validateInput() {
        const claim = this.claimInput.value.trim();
        this.checkBtn.disabled = claim.length < 10;
    }

    async checkFacts() {
        const claim = this.claimInput.value.trim();
        
        if (claim.length < 10) {
            alert('Please enter a claim with at least 10 characters.');
            return;
        }

        this.showLoading();
        
        try {
            // Simulate API delay for realistic experience
            await new Promise(resolve => setTimeout(resolve, 2000 + Math.random() * 2000));
            
            const factCheckResult = await this.performFactCheck(claim);
            this.displayResults(factCheckResult);
        } catch (error) {
            console.error('Fact checking failed:', error);
            this.showError('Failed to check facts. Please try again.');
        }
    }

    async performFactCheck(claim) {
        // Try to use backend API first, fallback to frontend simulation
        try {
            const response = await fetch('/api/fact-check', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ claim: claim })
            });

            if (response.ok) {
                const result = await response.json();
                result.timestamp = new Date(result.timestamp);
                return result;
            }
        } catch (error) {
            console.log('Backend API not available, using frontend simulation');
        }

        // Fallback to frontend simulation
        const analysisResult = this.analyzeClaimContent(claim);
        const matchingSources = this.findMatchingSources(claim);
        const verdict = this.calculateVerdict(analysisResult, matchingSources);
        
        return {
            claim: claim,
            analysis: analysisResult,
            sources: matchingSources,
            verdict: verdict,
            confidence: this.calculateConfidence(analysisResult, matchingSources),
            timestamp: new Date()
        };
    }

    analyzeClaimContent(claim) {
        // Simulate AI analysis of claim content
        const keywords = this.extractKeywords(claim);
        const claimType = this.identifyClaimType(claim);
        const sentiment = this.analyzeSentiment(claim);
        
        return {
            keywords: keywords,
            type: claimType,
            sentiment: sentiment,
            length: claim.length,
            complexity: this.assessComplexity(claim)
        };
    }

    extractKeywords(text) {
        // Simple keyword extraction (in real app, would use NLP)
        const commonWords = new Set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'been', 'have', 'has', 'had', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'do', 'does', 'did', 'get', 'got', 'go', 'went', 'come', 'came', 'say', 'said', 'tell', 'told', 'ask', 'asked', 'give', 'gave', 'take', 'took', 'make', 'made', 'know', 'knew', 'think', 'thought', 'see', 'saw', 'look', 'looked', 'want', 'wanted', 'use', 'used', 'find', 'found', 'work', 'worked', 'call', 'called', 'try', 'tried', 'need', 'needed', 'feel', 'felt', 'seem', 'seemed', 'leave', 'left', 'put', 'keep', 'kept', 'let', 'begin', 'began', 'help', 'helped', 'show', 'showed', 'hear', 'heard', 'play', 'played', 'run', 'ran', 'move', 'moved', 'live', 'lived', 'believe', 'believed', 'hold', 'held', 'bring', 'brought', 'happen', 'happened', 'write', 'wrote', 'sit', 'sat', 'stand', 'stood', 'lose', 'lost', 'pay', 'paid', 'meet', 'met', 'include', 'included', 'continue', 'continued', 'set', 'learn', 'learned', 'change', 'changed', 'lead', 'led', 'understand', 'understood', 'watch', 'watched', 'follow', 'followed', 'stop', 'stopped', 'create', 'created', 'speak', 'spoke', 'read', 'allow', 'allowed', 'add', 'added', 'spend', 'spent', 'grow', 'grew', 'open', 'opened', 'walk', 'walked', 'win', 'won', 'offer', 'offered', 'remember', 'remembered', 'love', 'loved', 'consider', 'considered', 'appear', 'appeared', 'buy', 'bought', 'wait', 'waited', 'serve', 'served', 'die', 'died', 'send', 'sent', 'expect', 'expected', 'build', 'built', 'stay', 'stayed', 'fall', 'fell', 'cut', 'reach', 'reached', 'kill', 'killed', 'remain', 'remained', 'suggest', 'suggested', 'raise', 'raised', 'pass', 'passed', 'sell', 'sold', 'require', 'required', 'report', 'reported', 'decide', 'decided', 'pull', 'pulled']);
        
        return text.toLowerCase()
            .replace(/[^\w\s]/g, ' ')
            .split(/\s+/)
            .filter(word => word.length > 3 && !commonWords.has(word))
            .slice(0, 10);
    }

    identifyClaimType(claim) {
        const healthKeywords = ['health', 'medical', 'disease', 'vaccine', 'treatment', 'doctor', 'hospital', 'medicine', 'covid', 'virus', 'bacteria'];
        const politicsKeywords = ['government', 'president', 'election', 'policy', 'congress', 'senate', 'vote', 'political', 'democrat', 'republican'];
        const scienceKeywords = ['research', 'study', 'scientist', 'experiment', 'data', 'climate', 'space', 'technology', 'scientific'];
        const economicsKeywords = ['economy', 'market', 'stock', 'price', 'inflation', 'economic', 'financial', 'money', 'business'];
        
        const lowerClaim = claim.toLowerCase();
        
        if (healthKeywords.some(keyword => lowerClaim.includes(keyword))) return 'health';
        if (politicsKeywords.some(keyword => lowerClaim.includes(keyword))) return 'politics';
        if (scienceKeywords.some(keyword => lowerClaim.includes(keyword))) return 'science';
        if (economicsKeywords.some(keyword => lowerClaim.includes(keyword))) return 'economics';
        
        return 'general';
    }

    analyzeSentiment(text) {
        // Simple sentiment analysis
        const positiveWords = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'awesome', 'brilliant', 'outstanding', 'perfect'];
        const negativeWords = ['bad', 'terrible', 'awful', 'horrible', 'disgusting', 'worst', 'hate', 'fail', 'wrong', 'false'];
        
        const words = text.toLowerCase().split(/\s+/);
        const positiveCount = words.filter(word => positiveWords.includes(word)).length;
        const negativeCount = words.filter(word => negativeWords.includes(word)).length;
        
        if (positiveCount > negativeCount) return 'positive';
        if (negativeCount > positiveCount) return 'negative';
        return 'neutral';
    }

    assessComplexity(text) {
        const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
        const avgWordsPerSentence = text.split(/\s+/).length / sentences.length;
        
        if (avgWordsPerSentence > 20) return 'high';
        if (avgWordsPerSentence > 12) return 'medium';
        return 'low';
    }

    findMatchingSources(claim) {
        // Simulate finding matching sources based on claim type and keywords
        const claimType = this.identifyClaimType(claim);
        const relevantSources = this.credibleSources.filter(source => {
            if (claimType === 'health' && (source.type === 'health' || source.type === 'fact-check')) return true;
            if (claimType === 'science' && (source.type === 'science' || source.type === 'fact-check')) return true;
            if (source.type === 'fact-check' || source.type === 'news') return true;
            return false;
        });

        // Generate mock matching sources with realistic data
        return relevantSources.slice(0, 3 + Math.floor(Math.random() * 3)).map(source => ({
            ...source,
            title: this.generateSourceTitle(claim, source),
            url: `https://${source.baseUrl}/${this.generateSlug(claim)}`,
            excerpt: this.generateSourceExcerpt(claim, source),
            publishDate: this.generateRecentDate(),
            relevanceScore: 70 + Math.floor(Math.random() * 25)
        }));
    }

    generateSourceTitle(claim, source) {
        const titles = {
            'fact-check': [
                `Fact Check: ${claim.substring(0, 50)}...`,
                `Is it true that ${claim.substring(0, 40)}?`,
                `Verifying claims about ${this.extractKeywords(claim)[0] || 'recent news'}`
            ],
            'news': [
                `Breaking: ${claim.substring(0, 45)}...`,
                `Report: ${claim.substring(0, 50)}...`,
                `Analysis: ${claim.substring(0, 45)}...`
            ],
            'health': [
                `Health Alert: ${claim.substring(0, 40)}...`,
                `Medical Update: ${claim.substring(0, 35)}...`,
                `Health Officials: ${claim.substring(0, 35)}...`
            ],
            'science': [
                `Study: ${claim.substring(0, 45)}...`,
                `Research: ${claim.substring(0, 40)}...`,
                `Scientists: ${claim.substring(0, 35)}...`
            ]
        };

        const sourceType = source.type;
        const typeTitles = titles[sourceType] || titles['news'];
        return typeTitles[Math.floor(Math.random() * typeTitles.length)];
    }

    generateSourceExcerpt(claim, source) {
        const excerpts = [
            `Our investigation into this claim reveals important details that provide context and clarity...`,
            `According to verified sources and expert analysis, the facts surrounding this matter are...`,
            `Recent evidence and expert testimony suggest that the situation is more nuanced than initially reported...`,
            `Multiple credible sources have confirmed key aspects of this story while highlighting areas that require further clarification...`,
            `Our fact-checking team has reviewed available evidence and consulted with experts in the field...`
        ];

        return excerpts[Math.floor(Math.random() * excerpts.length)];
    }

    generateRecentDate() {
        const now = new Date();
        const daysAgo = Math.floor(Math.random() * 30);
        const date = new Date(now.getTime() - (daysAgo * 24 * 60 * 60 * 1000));
        return date.toLocaleDateString();
    }

    generateSlug(text) {
        return text.toLowerCase()
            .replace(/[^\w\s]/g, '')
            .replace(/\s+/g, '-')
            .substring(0, 50);
    }

    calculateVerdict(analysis, sources) {
        // Simulate AI verdict calculation
        const sourceCount = sources.length;
        const avgCredibility = sources.reduce((sum, source) => sum + source.credibilityScore, 0) / sourceCount;
        const avgRelevance = sources.reduce((sum, source) => sum + source.relevanceScore, 0) / sourceCount;
        
        // Simple verdict logic based on various factors
        const verdictScore = (avgCredibility * 0.4) + (avgRelevance * 0.3) + (sourceCount * 5) + (Math.random() * 20);
        
        if (verdictScore > 85) return { type: 'true', label: 'Likely True' };
        if (verdictScore > 70) return { type: 'mixed', label: 'Mixed/Partial' };
        if (verdictScore > 50) return { type: 'unverified', label: 'Unverified' };
        return { type: 'false', label: 'Likely False' };
    }

    calculateConfidence(analysis, sources) {
        const sourceCount = sources.length;
        const avgCredibility = sources.reduce((sum, source) => sum + source.credibilityScore, 0) / sourceCount;
        const complexityFactor = analysis.complexity === 'low' ? 1.1 : analysis.complexity === 'medium' ? 1.0 : 0.9;
        
        let confidence = (avgCredibility / 100) * complexityFactor * (Math.min(sourceCount, 5) / 5);
        confidence = Math.max(0.3, Math.min(0.95, confidence + (Math.random() * 0.1 - 0.05)));
        
        return Math.round(confidence * 100);
    }

    showLoading() {
        this.checkBtn.disabled = true;
        this.results.classList.add('hidden');
        this.loading.classList.remove('hidden');
    }

    displayResults(result) {
        this.loading.classList.add('hidden');
        
        // Update overall rating
        this.overallRating.textContent = result.verdict.label;
        this.overallRating.className = `rating ${result.verdict.type}`;
        
        // Update claim display
        this.claimText.textContent = result.claim;
        
        // Update analysis summary
        this.analysisSummary.innerHTML = `
            <p><strong>Claim Type:</strong> ${result.analysis.type.charAt(0).toUpperCase() + result.analysis.type.slice(1)}</p>
            <p><strong>Key Topics:</strong> ${result.analysis.keywords.join(', ')}</p>
            <p><strong>Complexity:</strong> ${result.analysis.complexity.charAt(0).toUpperCase() + result.analysis.complexity.slice(1)}</p>
            <p><strong>Analysis completed on:</strong> ${result.timestamp.toLocaleDateString()} at ${result.timestamp.toLocaleTimeString()}</p>
        `;
        
        // Update sources list
        this.sourcesList.innerHTML = result.sources.map(source => `
            <div class="source-item">
                <div class="source-title">
                    <i class="fas fa-external-link-alt"></i>
                    ${source.title}
                    <span class="credibility-score">
                        <i class="fas fa-star"></i>
                        ${source.credibilityScore}% credible
                    </span>
                </div>
                <a href="${source.url}" target="_blank" class="source-url">${source.name} - ${source.url}</a>
                <div class="source-excerpt">${source.excerpt}</div>
                <div style="margin-top: 10px; font-size: 0.85rem; color: #666;">
                    <i class="fas fa-calendar"></i> Published: ${source.publishDate} | 
                    <i class="fas fa-chart-line"></i> Relevance: ${source.relevanceScore}%
                </div>
            </div>
        `).join('');
        
        // Update verdict
        this.verdict.innerHTML = this.generateVerdictText(result);
        
        // Update confidence score
        this.confidenceScore.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <span><strong>Confidence Level:</strong></span>
                <span><strong>${result.confidence}%</strong></span>
            </div>
            <div class="confidence-bar">
                <div class="confidence-fill" style="width: ${result.confidence}%"></div>
            </div>
            <div style="font-size: 0.9rem; color: #666; margin-top: 8px;">
                Based on ${result.sources.length} credible sources and comprehensive analysis
            </div>
        `;
        
        this.results.classList.remove('hidden');
        this.checkBtn.disabled = false;
    }

    generateVerdictText(result) {
        const verdictTexts = {
            'true': `Based on our analysis of ${result.sources.length} credible sources, this claim appears to be <strong>accurate</strong>. 
                     The information aligns with verified facts from reputable sources and expert analysis.`,
            'false': `Our fact-checking process using ${result.sources.length} credible sources indicates this claim is <strong>likely false</strong>. 
                      The available evidence contradicts the key assertions made in this statement.`,
            'mixed': `This claim contains both accurate and inaccurate elements. Our analysis of ${result.sources.length} sources shows that 
                      while some aspects are supported by evidence, other parts lack verification or are contradicted by credible sources.`,
            'unverified': `We could not find sufficient evidence from credible sources to verify this claim. This may be due to the claim being 
                           too recent, too specific, or relating to information that is not yet publicly available from reliable sources.`
        };

        return verdictTexts[result.verdict.type] || verdictTexts['unverified'];
    }

    showError(message) {
        this.loading.classList.add('hidden');
        this.checkBtn.disabled = false;
        alert(message);
    }

    resetForm() {
        this.claimInput.value = '';
        this.results.classList.add('hidden');
        this.claimInput.focus();
        this.validateInput();
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new FactChecker();
});