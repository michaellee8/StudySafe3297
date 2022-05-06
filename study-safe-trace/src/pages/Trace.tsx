import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
} from "@mui/material";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import React, { useContext, useState } from "react";
import { AxiosContext } from "../AxiosContext";
import { AdapterMoment } from "@mui/x-date-pickers/AdapterMoment";
import { DateTimePicker, LocalizationProvider } from "@mui/x-date-pickers";
import { DataGrid } from "@mui/x-data-grid";
import { height } from "@mui/system";
import { useNavigate } from "react-router";

interface TraceContact {
  id: number;
  hku_id: string;
  name: string;
}

interface TraceVenue {
  id: number;
  code: string;
  location: string;
  capacity: number;
}

interface TraceProps {
  logout: () => void;
}

export default function Trace({ logout }: TraceProps) {
  const axiosInstance = useContext(AxiosContext);
  const [studentUid, setStudentUid] = useState<string>("");
  const [startDateTime, setStartDateTime] = useState<Date | null>(null);
  const [endDateTime, setEndDateTime] = useState<Date | null>(null);
  const [alertOpen, setAlertOpen] = useState(false);
  const [alertErrorMessage, setAlertErrorMessage] = useState("");
  const [contacts, setContacts] = useState<TraceContact[]>([]);
  const [venues, setVenues] = useState<TraceVenue[]>([]);
  const navigate = useNavigate();

  const handleCloseDialog = () => {
    setAlertErrorMessage("");
    setAlertOpen(false);
  };

  const handleSignOut = () => {
    logout();
    navigate(`/signin`);
  };

  const handleQuery = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    try {
      if (!studentUid || !startDateTime || !endDateTime) {
        throw new Error("Please fill in all fields.");
      }
      const [contactsRes, venuesRes] = await Promise.all([
        axiosInstance.get<TraceContact[]>(`/studysafe/trace/contacts/`, {
          params: {
            hku_id: studentUid,
            start_datetime: startDateTime.toISOString(),
            end_datetime: endDateTime.toISOString(),
          },
        }),
        axiosInstance.get<TraceVenue[]>(`/studysafe/trace/venue/`, {
          params: {
            hku_id: studentUid,
            start_datetime: startDateTime.toISOString(),
            end_datetime: endDateTime.toISOString(),
          },
        }),
      ]);
      setContacts(contactsRes.data);
      setVenues(venuesRes.data);
    } catch (err) {
      setAlertErrorMessage(`${err}`);
      setAlertOpen(true);
    }
  };

  return (
    <LocalizationProvider dateAdapter={AdapterMoment}>
      <Container>
        <Box
          sx={{
            marginTop: 8,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <Typography component="h1" variant="h5">
            Contact tracing
          </Typography>
          <Box sx={{ mt: 1 }} component="form" onSubmit={handleQuery}>
            <TextField
              margin="normal"
              required
              fullWidth
              label="Student UID"
              type="text"
              id="student_uid"
              name="student_uid"
              value={studentUid}
              onChange={(event) => {
                setStudentUid(event.target.value);
              }}
            />
            <DateTimePicker
              label="Start DateTime"
              value={startDateTime}
              onChange={setStartDateTime}
              renderInput={(params) => <TextField {...params} />}
            />
            <DateTimePicker
              label="End DateTime"
              value={endDateTime}
              onChange={setEndDateTime}
              renderInput={(params) => <TextField {...params} />}
            />
            <Button
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              type="submit"
            >
              Search
            </Button>
          </Box>
          <Container style={{ height: "100%" }}>
            <Container>
              <Typography component="h1" variant="h5">
                Venues
              </Typography>
              <div style={{ height: 300, width: "100%" }}>
                <DataGrid
                  rows={venues}
                  columns={[
                    { field: "id", headerName: "ID", width: 150 },
                    { field: "code", headerName: "Code", width: 150 },
                    { field: "location", headerName: "Location", width: 150 },
                    { field: "capacity", headerName: "Capacity", width: 150 },
                  ]}
                />
              </div>
            </Container>
            <Container>
              <Typography component="h1" variant="h5">
                Contacts
              </Typography>
              <div style={{ height: 300, width: "100%" }}>
                <DataGrid
                  rows={contacts}
                  columns={[
                    { field: "id", headerName: "ID", width: 150 },
                    { field: "hku_id", headerName: "HKU ID", width: 150 },
                    { field: "name", headerName: "Name", width: 150 },
                  ]}
                />
              </div>
            </Container>
          </Container>
          <Button
            fullWidth
            variant="outlined"
            sx={{ mt: 3, mb: 2 }}
            onClick={handleSignOut}
          >
            Sign Out
          </Button>
        </Box>
        <Dialog open={alertOpen} onClose={handleCloseDialog}>
          <DialogTitle>{"Tracing failed"}</DialogTitle>
          <DialogContent>
            <DialogContentText>{alertErrorMessage}</DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog} autoFocus>
              Dismiss
            </Button>
          </DialogActions>
        </Dialog>
      </Container>
    </LocalizationProvider>
  );
}
