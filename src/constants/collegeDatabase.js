// src/constants/collegeDatabase.js

const getCompanies = (dept, tier) => {
  const top = {
    engineering: ["Google","Microsoft","Amazon","TCS","Infosys"],
    medical: ["AIIMS","Apollo Hospitals","Fortis"],
    arts_science: ["TCS","Infosys","Wipro","Cognizant"],
    law: ["Supreme Court","High Court","Tier-1 Law Firms"],
    management: ["McKinsey","BCG","Bain","Deloitte","KPMG"],
    agriculture: ["ICAR","State Agri Dept","ITC","Monsanto","Mahindra Agri"],
    pharmacy: ["Sun Pharma","Cipla","Dr Reddys"],
    architecture: ["Hafeez Contractor", "L&T Construction"],
    education: ["KV Schools", "International Schools"],
  };
  const mid = {
    engineering: ["TCS","Infosys","Cognizant","Wipro"],
    medical: ["Local Hospitals","Apollo","Fortis"],
    arts_science: ["TCS","BPO","Local Firms"],
    law: ["District Court","Law Firms"],
    management: ["TCS","Banks","HDFC","ICICI"],
    agriculture: ["State Agri Dept", "Local Agri Firms", "Fertilizer Companies"],
    pharmacy: ["Local Pharma", "Apollo Pharmacy"],
    architecture: ["Construction Companies", "Local Builders"],
    education: ["State Govt Schools", "Private Schools"],
  };
  return tier === "top" ? top[dept] || top.engineering : mid[dept] || mid.engineering;
};

const makeCollege = (name, location, state, dept, type, gender, rating, minPct, fee, placement, tier, hostel, naac, est, desc, courses, highlight) => ({
  name, location, state, department: dept, type, gender, rating, minPercentage: minPct,
  annualFee: fee, placementRate: placement, topCompanies: getCompanies(dept, tier),
  hostelAvailable: hostel, naacGrade: naac, established: est, description: desc,
  courses, highlight, mapQuery: name + " " + location + " " + state
});

// A curated list of top real colleges in India
const TOP_COLLEGES = [
  // Tamil Nadu - Engineering
  makeCollege("IIT Madras", "Chennai", "Tamil Nadu", "engineering", "Government", "Co-Education", 4.9, 98, "2,00,000", 99, "top", true, "A++", 1959, "Ranked #1 in India for Engineering", ["B.Tech", "M.Tech", "Ph.D"], "Top IIT in India"),
  makeCollege("NIT Trichy", "Tiruchirappalli", "Tamil Nadu", "engineering", "Government", "Co-Education", 4.8, 95, "1,50,000", 95, "top", true, "A++", 1964, "Top ranked NIT in India", ["B.Tech", "M.Tech"], "Top NIT"),
  makeCollege("Anna University (CEG)", "Chennai", "Tamil Nadu", "engineering", "Government", "Co-Education", 4.7, 92, "40,000", 90, "top", true, "A+", 1794, "Oldest engineering college in India", ["B.E", "B.Tech"], "State's Best Govt College"),
  makeCollege("VIT Vellore", "Vellore", "Tamil Nadu", "engineering", "Private", "Co-Education", 4.5, 85, "3,00,000", 92, "top", true, "A++", 1984, "Leading private institution with excellent placements", ["B.Tech"], "Highest Placement Offers"),
  makeCollege("SRM Institute of Science and Technology", "Kattankulathur", "Tamil Nadu", "engineering", "Private", "Co-Education", 4.3, 80, "2,50,000", 88, "top", true, "A++", 1985, "Huge campus with global exposure", ["B.Tech"], "Global Partnerships"),

  // Tamil Nadu - Medical
  makeCollege("Christian Medical College (CMC)", "Vellore", "Tamil Nadu", "medical", "Private", "Co-Education", 4.9, 97, "1,00,000", 99, "top", true, "A++", 1900, "One of the top medical colleges in India", ["MBBS", "BDS"], "World-class Hospital Attached"),
  makeCollege("Madras Medical College", "Chennai", "Tamil Nadu", "medical", "Government", "Co-Education", 4.8, 95, "18,000", 98, "top", true, "A+", 1835, "Oldest medical college in India", ["MBBS", "BDS"], "Govt Top Choice"),
  
  // Tamil Nadu - Agriculture
  makeCollege("Tamil Nadu Agricultural University (TNAU)", "Coimbatore", "Tamil Nadu", "agriculture", "Government", "Co-Education", 4.8, 88, "45,000", 85, "top", true, "A++", 1971, "Leading agricultural university in India", ["B.Sc Agriculture", "B.Tech Agriculture"], "ICAR Recognized Top University"),
  makeCollege("Annamalai University (Faculty of Agriculture)", "Chidambaram", "Tamil Nadu", "agriculture", "Government", "Co-Education", 4.2, 75, "60,000", 70, "mid", true, "A", 1929, "Historic university with vast agricultural land", ["B.Sc Agriculture"], "Large Agricultural Farms"),

  // Maharashtra - Engineering
  makeCollege("IIT Bombay", "Mumbai", "Maharashtra", "engineering", "Government", "Co-Education", 5.0, 99, "2,20,000", 99, "top", true, "A++", 1958, "Premier engineering institute in India", ["B.Tech"], "Unmatched Placements"),
  makeCollege("College of Engineering Pune (COEP)", "Pune", "Maharashtra", "engineering", "Government", "Co-Education", 4.7, 94, "90,000", 92, "top", true, "A+", 1854, "One of the oldest and best state engineering colleges", ["B.Tech"], "Rich Heritage"),
  makeCollege("VJTI", "Mumbai", "Maharashtra", "engineering", "Government", "Co-Education", 4.6, 92, "85,000", 90, "top", false, "A", 1887, "Prestigious state college in Mumbai", ["B.Tech"], "Excellent Mumbai Placements"),

  // Maharashtra - Agriculture
  makeCollege("Mahatma Phule Krishi Vidyapeeth (MPKV)", "Rahuri", "Maharashtra", "agriculture", "Government", "Co-Education", 4.6, 82, "40,000", 80, "top", true, "A+", 1968, "Premier agriculture university in Maharashtra", ["B.Sc Agriculture"], "Top Agri Research"),

  // Delhi - Engineering & Medical
  makeCollege("IIT Delhi", "New Delhi", "Delhi", "engineering", "Government", "Co-Education", 4.9, 98, "2,10,000", 98, "top", true, "A++", 1961, "Eminent engineering institution", ["B.Tech"], "Capital City Exposure"),
  makeCollege("AIIMS New Delhi", "New Delhi", "Delhi", "medical", "Government", "Co-Education", 5.0, 99, "5,000", 100, "top", true, "A++", 1956, "The best medical college in India", ["MBBS"], "Best Medical Infrastructure"),
  
  // Delhi - Agriculture
  makeCollege("Indian Agricultural Research Institute (IARI)", "New Delhi", "Delhi", "agriculture", "Government", "Co-Education", 4.9, 90, "30,000", 90, "top", true, "A++", 1905, "The seat of India's Green Revolution", ["B.Sc Agriculture", "M.Sc"], "Seat of Green Revolution"),

  // Karnataka - Engineering & Agriculture
  makeCollege("NITK Surathkal", "Mangalore", "Karnataka", "engineering", "Government", "Co-Education", 4.8, 96, "1,40,000", 94, "top", true, "A++", 1960, "Top NIT in Karnataka", ["B.Tech"], "Private Beach Campus"),
  makeCollege("University of Agricultural Sciences (UAS)", "Bangalore", "Karnataka", "agriculture", "Government", "Co-Education", 4.7, 85, "50,000", 82, "top", true, "A+", 1964, "Top agricultural university in Karnataka", ["B.Sc Agriculture"], "Silicon Valley Agri-Tech"),

  // Telangana/AP
  makeCollege("IIT Hyderabad", "Hyderabad", "Telangana", "engineering", "Government", "Co-Education", 4.7, 95, "2,00,000", 93, "top", true, "A++", 2008, "Fastest growing new IIT", ["B.Tech"], "Innovative Curriculum"),
  makeCollege("Professor Jayashankar Telangana State Agricultural University", "Hyderabad", "Telangana", "agriculture", "Government", "Co-Education", 4.5, 80, "45,000", 78, "top", true, "A", 2014, "State's best agri university", ["B.Sc Agriculture"], "Modern Agri Methods"),
];

import collegesData from './colleges_compressed.json';

const PARSED_COLLEGES = collegesData.map(c => ({
  name: c[0],
  location: c[1],
  state: c[2],
  department: c[3],
  type: c[4],
  gender: "Co-Education",
  rating: c[5],
  placementRate: c[6],
  minPercentage: c[7],
  annualFee: "Contact College",
  topCompanies: getCompanies(c[3], "mid"),
  hostelAvailable: c[8] === 1,
  naacGrade: "B+",
  established: 2000,
  description: `A ${c[4].toLowerCase()} college located in ${c[1]}, ${c[2]}.`,
  courses: ["Various Courses"],
  highlight: "",
  mapQuery: `${c[0]} ${c[1]} ${c[2]}`
}));

// Combine curated top colleges with parsed ones
export const COLLEGE_DATABASE = [...TOP_COLLEGES, ...PARSED_COLLEGES];


export const getCollegesForStudent = (state, department, percentage, entranceScore = 0) => {
  // 1. Filter by exactly the chosen department
  let deptMatch = COLLEGE_DATABASE.filter(c => c.department === department);
  if (deptMatch.length === 0) {
    // If department has no colleges, use all colleges as fallback
    deptMatch = COLLEGE_DATABASE;
  }
  
  // 2. Filter out colleges where student percentage is too low
  // Give +5% leeway to show colleges they are close to getting into
  const eligible = deptMatch.filter(c => percentage >= (c.minPercentage - 5));

  // 3. Separate into "Same State" and "Other States"
  const stateMatch = eligible.filter(c => c.state.toLowerCase() === (state || "").toLowerCase());
  const others = eligible.filter(c => c.state.toLowerCase() !== (state || "").toLowerCase());

  // 4. Sort both arrays: Best Rating first, then Lower Cutoff first
  const sortFunc = (a, b) => {
    if (b.rating !== a.rating) return b.rating - a.rating;
    return a.minPercentage - b.minPercentage;
  };
  
  stateMatch.sort(sortFunc);
  others.sort(sortFunc);

  // 5. Combine: Put same-state colleges at the top
  let combined = [...stateMatch, ...others];

  // If no colleges found, return some suggestions from the same department to avoid an empty screen
  if (combined.length === 0) {
    combined = deptMatch.sort((a,b) => a.minPercentage - b.minPercentage).slice(0, 15);
  }

  return combined;
};

export const searchColleges = (query) => {
  if (!query) return COLLEGE_DATABASE.slice(0, 20);
  const q = query.toLowerCase();
  return COLLEGE_DATABASE.filter(c =>
    c.name.toLowerCase().includes(q) ||
    c.location.toLowerCase().includes(q) ||
    c.state.toLowerCase().includes(q) ||
    c.department.toLowerCase().includes(q) ||
    c.type.toLowerCase().includes(q)
  ).slice(0, 100); // Limit search results for performance
};
