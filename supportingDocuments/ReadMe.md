# 🎵 Welcome to Gigify

This lightweight Flask application allows you to connect to your Spotify account and creates a custom playlist based on upcoming gigs in your area and your listening preferences.

## 🚀 Current Functionality

### 🔧 Backend Local Deployment

- You can run the Flask application `gigify.py` and use manual URL routing.
- The following URLs are routed as API endpoints for the frontend:
  - `/events/bristol` — enter a city you'd like to query Ticketmaster about
  - `/artists/pixies` — enter an artist you'd like to query Spotify about

### 🌐 API Integration

- Currently working on `APIIntegration.py`, a script pulling separate API calls together.
- Challenges include:
  - IP location services returning overly localized locations (e.g. "Windsor" instead of "London"), which are not always recognized by the Ticketmaster API.

---

## ✅ Project Checklist

### 1. Setup
- [✅] Create Flask backend project  
- [✅] Create React frontend with Vite or CRA  
- [✅] Enable CORS between frontend and backend  
- [✅] Connect frontend to backend locally (test with `/ping` route)  

---

### 2. Spotify Integration (Backend)
- [✅] Register Spotify app  
- [✅] Set `REDIRECT_URI` and environment variables  
- [✅] Implement `/login` route (redirect to Spotify auth)  
- [✅] Implement `/callback` to:  
-[✅] Exchange code for `access_token`  
  - Store token in Flask session  
- [ ] Implement `get_top_artists()` helper  

---

### 3. Ticketmaster Integration (Backend)
- [✅ ] Register for Ticketmaster API key  
- [✅ ] Create `get_ticketmaster_events()` function  
- [✅ ] Implement `/events` route to return events near a city  

---

### 4. Artist Matching Logic
- [ ] Compare Spotify top artists with Ticketmaster event artists  
- [ ] Clean/normalize artist names (case, punctuation)  
- [ ] Return matched events and artist names  

---

### 5. Spotify Playlist Creation
- [ ] Get user profile (`/v1/me`)  
- [ ] Create a new playlist  
- [ ] Search for tracks from matching artists  
- [ ] Add tracks to the playlist  
- [ ] Return playlist URL in response  

---

### 6. React Frontend
- [ ] Landing page with:  
  - “Log in with Spotify” button (calls `/login`)  
- [ ] Post-login state:  
  - Display loading spinner/message  
  - Show matched events  
  - “Create Playlist” button  
  - Display success message and link to Spotify playlist  
- [ ] Add styling with Material UI templates  

---

### 7. Deployment
- [ ] Deploy Flask backend (Render / Railway / Fly.io)  
- [ ] Set Spotify API keys as environment variables  
- [ ] Deploy React frontend (Netlify / Vercel)  
- [ ] Update `REDIRECT_URI` for production  
- [ ] Test full flow end-to-end in production  
