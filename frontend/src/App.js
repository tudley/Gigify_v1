/*
import React, { useEffect, useState } from 'react';

function App() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/events')
      .then(response => response.json())
      .then(data => setEvents(data));
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Upcoming Events</h1>
      <ul>
        {events.map(event => (
          <li key={event.id}>
            <strong>{event.name}</strong> – {event.location} on {event.date}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;

*/

import React, { useEffect, useState } from 'react';
import {
  Container,
  Typography,
  Card,
  CardContent,
  Grid,
  CssBaseline,
  Button,
} from '@mui/material';

function App() {
  const [events, setEvents] = useState([]);
  const [location, setLocation] = useState('');

  useEffect(() => {
    fetch('http://localhost:5000/events')
      .then(res => res.json())
      .then(data => setEvents(data));
  }, []);

  const handleSpotifyLogin = () => {
    // Redirect to Flask backend to start the Spotify login process
    window.location.href = "http://localhost:5000/login";
  };

  return (
    <>
      <CssBaseline />
      <Container maxWidth="md" style={{ marginTop: '2rem' }}>
        <Typography variant="h4" gutterBottom>
          Upcoming Events
        </Typography>

        <Button
          variant="contained"
          color="primary"
          onClick={handleSpotifyLogin}
          style={{ marginBottom: '2rem' }}
        >
          Login with Spotify
        </Button>

        <Grid container spacing={2}>
          {events.map(event => (
            <Grid item xs={12} sm={6} md={4} key={event.id}>
              <Card>
                <CardContent>
                  <Typography variant="h6">{event.name}</Typography>
                  <Typography color="textSecondary">{event.location}</Typography>
                  <Typography color="textSecondary">{event.date}</Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>
    </>
  );
}

export default App;

