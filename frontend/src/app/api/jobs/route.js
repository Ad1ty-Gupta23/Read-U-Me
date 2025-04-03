import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';
import { parse } from 'csv-parse/sync';

export async function GET() {
  try {
    // Path to the LinkedIn jobs CSV file
    const csvPath = path.join(process.cwd(), 'linkedin_jobs_india.csv');
    console.log(csvPath);
    // Read the CSV file
    const fileContent = fs.readFileSync(csvPath, 'utf8');
    console.log(fileContent);
    // Parse the CSV content
    const records = parse(fileContent, {
      columns: true,
      skip_empty_lines: true
    });
    
    return NextResponse.json({ jobs: records });
  } catch (error) {
    console.error('Error fetching jobs:', error);
    return NextResponse.json(
      { error: error.message || 'Failed to fetch jobs' },
      { status: 500 }
    );
  }
}