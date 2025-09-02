# Derk's Gym AI Web Dashboard

## 🎯 Overview

The Derk's Gym AI Web Dashboard is a comprehensive visualization system for managing and analyzing your derkling teams, battle performance, and strategic relationships. It provides an intuitive web interface to view all your fighter profiles, team compositions, and battle metrics in one place.

## 🚀 Quick Start

### Starting the Dashboard

**Windows:**
```bash
start_dashboard.bat
```

**Linux/Mac:**
```bash
./start_dashboard.sh
```

The dashboard will be available at: **http://localhost:5000**

### Manual Start
```bash
cd web_dashboard
python -m flask run --host=0.0.0.0 --port=5000
```

## 📋 Features

### 1. Main Dashboard (`/`)
- **Team Overview Cards**: Visual representation of all derkling teams
- **Individual Derkling Profiles**: Quick access to fighter details
- **Quick Stats**: Total derklings, active teams, battles completed, win rate
- **Equipment & Bounty Summary**: Key loadout and reward information

### 2. Teams Page (`/teams`)
- **Team Compositions**: Detailed view of each team's members
- **Fighter Bonds & Compatibility**: Relationship mapping between derklings
- **Strategy Loadouts**: Predefined team formations for different battle scenarios
- **Synergy Visualization**: How fighters complement each other

### 3. Project Number Eleven (`/number_eleven`)
- **Classified Development Tracking**: Special experimental derkling project
- **Development Phases**: Progress tracking through design, implementation, testing
- **Theoretical Capabilities**: Projected performance metrics
- **Radar Chart Comparison**: Visual comparison with standard derklings

### 4. Battle Metrics (`/battles`)
- **Performance Overview**: Win/loss statistics and trends
- **Interactive Charts**: 
  - Win/Loss distribution (pie chart)
  - Team performance comparison (bar chart)
  - Rolling win rate trends (line chart)
- **Battle History**: Recent battle results with detailed information
- **Performance Analytics**: Statistical analysis of combat effectiveness

## 🎨 Visual Design

### Color Coding
- **Peanuts Team**: Brown/Tan (#8B4513 / #D2B48C)
- **Testing Team**: Blue/Gold (#4169E1 / #FFD700)
- **Special Team**: Dark Red/Tomato (#8B0000 / #FF6347)
- **Lone Wolf**: Dark Slate Gray (#2F4F4F / #778899)

### Interactive Elements
- **Hover Effects**: Cards lift and glow on hover
- **Color Previews**: Visual color swatches for derkling themes
- **Progress Bars**: Team spirit and development progress visualization
- **Responsive Design**: Works on desktop, tablet, and mobile

## 📊 Data Sources

### API Endpoints
- `/api/derklings` - Individual derkling configurations
- `/api/teams` - Team organization data
- `/api/relationships` - Fighter bonds and compatibility
- `/api/battle_history` - Historical battle results

### Data Integration
- **Brain Classes**: Automatically extracts data from Python brain files
- **Battle Results**: Reads JSON files from the `results/` directory
- **Real-time Updates**: Refresh page to see latest battle data

## 🔧 Technical Details

### Technology Stack
- **Backend**: Flask (Python web framework)
- **Frontend**: Bootstrap 5 + Custom CSS
- **Charts**: Chart.js for interactive visualizations
- **Icons**: Font Awesome 6
- **Layout**: Responsive grid system

### File Structure
```
web_dashboard/
├── app.py                  # Flask application
├── requirements.txt        # Python dependencies
├── templates/             # HTML templates
│   ├── index.html         # Main dashboard
│   ├── teams.html         # Teams overview
│   ├── number_eleven.html # Special project
│   └── battles.html       # Battle metrics
└── static/               # Static assets
    ├── css/
    │   └── dashboard.css  # Custom styles
    └── js/
        ├── dashboard.js   # Main dashboard logic
        ├── teams.js       # Teams page logic
        └── battles.js     # Battle metrics logic
```

## 📈 Customization

### Adding New Derklings
1. Create a new brain class in `src/brain_profiles/`
2. Implement the `get_derk_gym_config()` method
3. Add import to `web_dashboard/app.py`
4. Restart the dashboard

### Team Relationships
Edit the `api_relationships()` function in `app.py` to define:
- **Core Teams**: Primary team compositions
- **Fighter Bonds**: Which derklings work well together
- **Strategies**: Different tactical approaches

### Custom Styling
Modify `static/css/dashboard.css` to:
- Change team colors
- Adjust card layouts
- Add new visual effects
- Customize responsive breakpoints

## 🛠️ Troubleshooting

### Common Issues

**Dashboard won't start:**
- Ensure Flask is installed: `pip install flask`
- Check if port 5000 is available
- Verify you're in the correct directory

**Missing derkling data:**
- Check brain class imports in `app.py`
- Ensure `get_derk_gym_config()` method exists
- Verify file paths are correct

**Charts not displaying:**
- Check browser console for JavaScript errors
- Ensure Chart.js is loading (check network tab)
- Verify data format in API responses

**Battle history empty:**
- Check `results/` directory for JSON files
- Verify battle result file format
- Check file permissions

### Debug Mode
Set `FLASK_DEBUG=true` for detailed error messages and auto-reload.

## 🎯 Future Enhancements

### Planned Features
- **Real-time Battle Streaming**: Live updates during battles
- **Advanced Analytics**: Machine learning insights
- **Team Builder**: Drag-and-drop team composition
- **Export Functionality**: PDF reports and data export
- **Mobile App**: Native mobile application
- **Multi-user Support**: Team collaboration features

### Integration Opportunities
- **Steam Game Integration**: Compare with actual Steam game data
- **Discord Bot**: Battle notifications and stats
- **API Extensions**: RESTful API for external tools
- **Database Backend**: Persistent data storage

## 📝 Development Notes

### Code Organization
- **Modular Design**: Separate JavaScript files for each page
- **API-First**: Clean separation between backend and frontend
- **Responsive**: Mobile-first design approach
- **Accessible**: ARIA labels and keyboard navigation

### Performance Considerations
- **Lazy Loading**: Charts load only when needed
- **Caching**: Static assets cached by browser
- **Optimization**: Minified CSS/JS in production
- **Scalability**: Designed for larger datasets

---

**Happy Derkling Management!** 🤖⚔️
