// Battles page JavaScript

class BattlesPage {
    constructor() {
        this.battleHistory = [];
        this.charts = {};
        this.init();
    }

    async init() {
        await this.loadBattleData();
        this.updateStatistics();
        this.createCharts();
        this.renderBattleHistory();
    }

    async loadBattleData() {
        try {
            const response = await fetch('/api/battle_history');
            this.battleHistory = await response.json();
        } catch (error) {
            console.error('Error loading battle data:', error);
            // Create mock data for demonstration
            this.battleHistory = this.createMockBattleData();
        }
    }

    createMockBattleData() {
        // Create some mock battle data for demonstration
        const teams = ['peanuts', 'testing', 'special', 'lone_wolf'];
        const results = ['victory', 'defeat', 'draw'];
        const mockData = [];

        for (let i = 0; i < 20; i++) {
            mockData.push({
                id: i + 1,
                date: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString(),
                homeTeam: teams[Math.floor(Math.random() * teams.length)],
                awayTeam: teams[Math.floor(Math.random() * teams.length)],
                result: results[Math.floor(Math.random() * results.length)],
                score: {
                    home: Math.floor(Math.random() * 1000),
                    away: Math.floor(Math.random() * 1000)
                },
                duration: Math.floor(Math.random() * 300) + 60
            });
        }

        return mockData;
    }

    updateStatistics() {
        const victories = this.battleHistory.filter(b => b.result === 'victory').length;
        const defeats = this.battleHistory.filter(b => b.result === 'defeat').length;
        const draws = this.battleHistory.filter(b => b.result === 'draw').length;
        const total = this.battleHistory.length;
        const winRate = total > 0 ? Math.round((victories / total) * 100) : 0;

        document.getElementById('total-victories').textContent = victories;
        document.getElementById('total-defeats').textContent = defeats;
        document.getElementById('total-draws').textContent = draws;
        document.getElementById('win-rate-display').textContent = `${winRate}%`;
    }

    createCharts() {
        this.createWinLossChart();
        this.createTeamPerformanceChart();
        this.createTrendChart();
    }

    createWinLossChart() {
        const ctx = document.getElementById('winLossChart').getContext('2d');
        const victories = this.battleHistory.filter(b => b.result === 'victory').length;
        const defeats = this.battleHistory.filter(b => b.result === 'defeat').length;
        const draws = this.battleHistory.filter(b => b.result === 'draw').length;

        this.charts.winLoss = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Victories', 'Defeats', 'Draws'],
                datasets: [{
                    data: [victories, defeats, draws],
                    backgroundColor: ['#28a745', '#dc3545', '#ffc107'],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    createTeamPerformanceChart() {
        const ctx = document.getElementById('teamPerformanceChart').getContext('2d');
        
        // Calculate team performance
        const teams = ['peanuts', 'testing', 'special', 'lone_wolf'];
        const teamStats = {};

        teams.forEach(team => {
            const teamBattles = this.battleHistory.filter(b => 
                b.homeTeam === team || b.awayTeam === team
            );
            const wins = teamBattles.filter(b => b.result === 'victory').length;
            teamStats[team] = teamBattles.length > 0 ? (wins / teamBattles.length) * 100 : 0;
        });

        this.charts.teamPerformance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: teams.map(t => t.replace('_', ' ').toUpperCase()),
                datasets: [{
                    label: 'Win Rate (%)',
                    data: Object.values(teamStats),
                    backgroundColor: ['#8B4513', '#4169E1', '#8B0000', '#2F4F4F'],
                    borderColor: ['#654321', '#1E3A8A', '#660000', '#1C3333'],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });
    }

    createTrendChart() {
        const ctx = document.getElementById('trendChart').getContext('2d');
        
        // Create rolling win rate over time
        const sortedBattles = [...this.battleHistory].sort((a, b) => new Date(a.date) - new Date(b.date));
        const trendData = [];
        const labels = [];
        
        const windowSize = 5; // Rolling window of 5 battles
        
        for (let i = windowSize - 1; i < sortedBattles.length; i++) {
            const window = sortedBattles.slice(i - windowSize + 1, i + 1);
            const wins = window.filter(b => b.result === 'victory').length;
            const winRate = (wins / windowSize) * 100;
            
            trendData.push(winRate);
            labels.push(`Battle ${i + 1}`);
        }

        this.charts.trend = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Rolling Win Rate (5 battles)',
                    data: trendData,
                    borderColor: '#007bff',
                    backgroundColor: 'rgba(0, 123, 255, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });
    }

    renderBattleHistory() {
        const container = document.getElementById('battle-history-table');
        if (!container) return;

        const recentBattles = [...this.battleHistory]
            .sort((a, b) => new Date(b.date) - new Date(a.date))
            .slice(0, 10);

        container.innerHTML = `
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Home Team</th>
                            <th>Away Team</th>
                            <th>Result</th>
                            <th>Score</th>
                            <th>Duration</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${recentBattles.map(battle => `
                            <tr>
                                <td>${new Date(battle.date).toLocaleDateString()}</td>
                                <td>
                                    <span class="badge team-${battle.homeTeam}">
                                        ${battle.homeTeam.replace('_', ' ').toUpperCase()}
                                    </span>
                                </td>
                                <td>
                                    <span class="badge team-${battle.awayTeam}">
                                        ${battle.awayTeam.replace('_', ' ').toUpperCase()}
                                    </span>
                                </td>
                                <td>
                                    <span class="badge ${this.getResultBadgeClass(battle.result)}">
                                        ${battle.result.toUpperCase()}
                                    </span>
                                </td>
                                <td>${battle.score?.home || 0} - ${battle.score?.away || 0}</td>
                                <td>${Math.floor(battle.duration / 60)}:${String(battle.duration % 60).padStart(2, '0')}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }

    getResultBadgeClass(result) {
        const classes = {
            'victory': 'bg-success',
            'defeat': 'bg-danger',
            'draw': 'bg-warning'
        };
        return classes[result] || 'bg-secondary';
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new BattlesPage();
});
