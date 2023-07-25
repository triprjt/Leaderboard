import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import Table from "react-bootstrap/Table";
import Button from "react-bootstrap/Button";
import Tab from "react-bootstrap/Tab";
import Tabs from "react-bootstrap/Tabs";
import "bootstrap/dist/css/bootstrap.min.css";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import InputGroup from "react-bootstrap/InputGroup";
import FormControl from "react-bootstrap/FormControl";
import Dropdown from "react-bootstrap/Dropdown";
import "./App.css";

function StudentList() {
  const [timeframe, setTimeframe] = useState("all");
  const rollNumberRef = useRef();

  const [rollNumber, setRollNumber] = useState("");
  const [students, setStudents] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [studentData, setStudentData] = useState({}); // to store the student data
  const [filterData, setFilterData] = useState({});

  const handleTabClick = (key) => {
    setTimeframe(key === "all" ? "all" : "week");
  };

  const renderTable = (studentsList) => {
    // Identify the rank of the entered student
    let studentRank = null;
    let rollNumberInt = parseInt(rollNumber);
    if (rollNumberInt) {
      const studentIndex = studentsList.findIndex(
        (student) => student.roll_no === rollNumberInt
      );
      if (studentIndex !== -1) {
        studentRank = studentIndex + 1; // ranks start at 1
      }
    }
    return (
      <Container>
        <Row className="justify-content-md-center">
          <Col md="auto">
            <div className="table-container mobile-table-container">
              <div className="scrollable-table scrollable-table-mobile">
                <Table striped bordered hover className="mobile-table">
                  <thead>
                    <tr>
                      <th>Rank</th>
                      <th>Roll Number</th>
                      <th>Grade</th>
                      <th>Name</th>
                      <th>School</th>
                      <th>Section</th>
                      <th>Points</th>
                    </tr>
                  </thead>
                  <tbody>
                    {!isLoading &&
                      studentsList.map((student, index) => {
                        // Add sticky class if the roll number matches and its rank is outside top 10
                        const isStickyRow =
                          rollNumberInt === student.roll_no && studentRank > 10;
                        // Add highlight class if the student's rank is equal to studentRank
                        const isHighlightedRow = index + 1 === studentRank; // Define class names based on whether this is a highlighted row or not

                        let classNames = isStickyRow ? "sticky-row" : "";
                        classNames += isHighlightedRow ? " highlight" : "";

                        return (
                          <tr key={index} className={classNames}>
                            <td>{index + 1}</td>
                            <td>{student.roll_no}</td>
                            <td>{student.grade}</td>
                            <td>{student.name}</td>
                            <td>{student.school_name}</td>
                            <td>{student.section_name}</td>
                            <td>{student.points}</td>
                          </tr>
                        );
                      })}
                  </tbody>
                </Table>
              </div>
              <div>
                {rollNumber &&
                  !studentsList.some(
                    (student) => student.roll_no === rollNumberInt
                  ) && (
                    <p className="text-danger">Your name is not on the list</p>
                  )}
              </div>
            </div>
          </Col>
        </Row>
      </Container>
    );
  };

  // 1. create useEffect to fetch initial results from the API

  useEffect(() => {
    const fetchAllStudents = async () => {
      setIsLoading(true); // set isLoading to true before the data fetching begins
      try {
        const response = await axios.get(
          `${process.env.REACT_APP_API_URL}students/`
        );
        setStudents(response.data); // store the students data in state
      } catch (error) {
        console.error("Error fetching all students:", error);
      } finally {
        setIsLoading(false); // set isLoading to false after the data fetching completes (either successfully or with an error)
      }
    };

    fetchAllStudents();
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setRollNumber(rollNumberRef.current.value);

    // Validation
    const rollNumberInt = parseInt(rollNumberRef.current.value);
    if (isNaN(rollNumberInt) || rollNumberInt > 1000) {
      alert("Please enter a valid roll number");
      return;
    }

    const response = await axios.get(
      `${process.env.REACT_APP_API_URL}students/by_roll_no/`,
      {
        params: { roll_no: rollNumberInt },
      }
    );
    setFilterData({ filterType: "none", filterValue: "" });
    setStudentData(response.data[0]);
    console.log(response.data[0]);
  };

  useEffect(() => {
    const filterStudents = async () => {
      let response;
      let responseData = [];
      if (filterData.filterType && filterData.filterValue) {
        if (filterData.filterType === "friends") {
          try {
            response = await axios.get(
              `${process.env.REACT_APP_API_URL}students/by_friends/`,
              {
                params: {
                  roll_no: filterData.filterValue,
                },
              }
            );
            let studentData = response.data.student;
            let friendsData = response.data.friends;
            responseData = [studentData, ...friendsData];
          } catch (error) {
            console.error("Error fetching all friends:", error);
          }
        } else {
          try {
            response = await axios.get(
              `${process.env.REACT_APP_API_URL}students/by_filter/`,
              {
                params: {
                  type: filterData.filterType,
                  value: filterData.filterValue,
                },
              }
            );
            responseData = response.data;
          } catch (error) {
            console.error("Error fetching all students:", error);
          }
        }
      } else {
        try {
          response = await axios.get(
            `${process.env.REACT_APP_API_URL}students/`
          );
          responseData = response.data;
        } catch (error) {
          console.error("Error fetching all students:", error);
        }
      }

      // apply time filters-'All' and 'last week'
      const oneWeekAgo = new Date();
      oneWeekAgo.setDate(oneWeekAgo.getDate() - 7); // get the date one week ago

      // If timeframe is 'week', filter the students to those updated within the last week
      if (timeframe === "week") {
        responseData = responseData.filter((student) => {
          const studentDate = new Date(student.updated_at);
          return studentDate > oneWeekAgo;
        });
      }
      setStudents(responseData);
    };
    filterStudents();
  }, [filterData, timeframe]);

  return (
    <div className="">
      <Form onSubmit={handleSubmit} className="w-100 w-md-50 mx-auto formtop">
        <InputGroup className="mb-3 mx-auto d-flex justify-content-center">
          <div className="col-4 col-lg-2">
            <InputGroup.Text
              id="basic-addon1"
              className="w-100 justify-content-center"
            >
              Roll Number
            </InputGroup.Text>
          </div>
          <div className="col-8 col-lg-3 justify-content-center">
            <FormControl
              placeholder="Enter roll number"
              aria-label="Roll Number"
              aria-describedby="basic-addon1"
              ref={rollNumberRef}
              className="w-100 "
            />
          </div>
        </InputGroup>

        <div className="d-flex justify-content-center inputbutton">
          <Button variant="primary" type="submit">
            Submit
          </Button>

          <Dropdown
            onSelect={(eventKey) =>
              setFilterData({
                filterType: eventKey,
                filterValue:
                  eventKey === "friends"
                    ? studentData.roll_no
                    : studentData[eventKey],
              })
            }
          >
            <Dropdown.Toggle variant="secondary" id="dropdown-basic">
              Filter
            </Dropdown.Toggle>
            <Dropdown.Menu>
              <Dropdown.Item eventKey="school_id">My school</Dropdown.Item>
              <Dropdown.Item eventKey="section_id">My section</Dropdown.Item>
              <Dropdown.Item eventKey="grade">My grade</Dropdown.Item>
              <Dropdown.Item eventKey="friends">My friends</Dropdown.Item>
              <Dropdown.Item eventKey="none">None</Dropdown.Item>
            </Dropdown.Menu>
            {filterData && <ShowSelectedFilter filterData={filterData} />}
          </Dropdown>
        </div>
      </Form>

      <div>
        <Tabs
          defaultActiveKey="all"
          onSelect={handleTabClick}
          className="mx-auto"
        >
          <Tab eventKey="all" title="All time">
            {students && (
              <Table className="custom-table">{renderTable(students)}</Table>
            )}
          </Tab>
          <Tab eventKey="week" title="Last week">
            {students && (
              <Table className="custom-table">{renderTable(students)}</Table>
            )}
          </Tab>
        </Tabs>
      </div>
    </div>
  );
}

export default StudentList;

function ShowSelectedFilter({ filterData }) {
  switch (filterData.filterType) {
    case "school_id":
      return <span> My School</span>;
    case "section_id":
      return <span> My section</span>;
    case "grade":
      return <span> My grade</span>;
    case "friends":
      return <span> My friends</span>;
    default:
      return null;
  }
}
