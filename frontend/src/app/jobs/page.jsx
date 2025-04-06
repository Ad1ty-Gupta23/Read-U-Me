"use client";

import { useState, useEffect } from 'react';
import Link from 'next/link';

export default function JobsPage() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('');

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await fetch('/api/jobs');
        
        if (!response.ok) {
          throw new Error('Failed to fetch jobs');
        }
        
        const data = await response.json();
        setJobs(data.jobs || []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    
    fetchJobs();
  }, []);

  // Filter jobs based on search term and filter type
  const filteredJobs = jobs.filter(job => {
    const matchesSearch = searchTerm === '' || 
      job.job_title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      job.company_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      job.job_location?.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesFilter = filterType === '' || 
      job.job_type_skills?.toLowerCase().includes(filterType.toLowerCase());
    
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">LinkedIn Job Listings</h1>
          <p className="mt-2 text-lg text-gray-600">Browse through available job opportunities</p>
        </div>

        {/* Search and Filter */}
        <div className="mb-8 flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <input
              type="text"
              placeholder="Search jobs, companies, or locations..."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <div className="sm:w-64">
            <select
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
            >
              <option value="">All Job Types</option>
              <option value="Software">Software</option>
              <option value="Data Science">Data Science</option>
              <option value="Marketing">Marketing</option>
              <option value="Design">Design</option>
              <option value="Management">Management</option>
            </select>
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="text-center py-12">
            <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-blue-600 border-r-transparent"></div>
            <p className="mt-4 text-gray-600">Loading jobs...</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="text-center py-12">
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
              <strong className="font-bold">Error: </strong>
              <span className="block sm:inline">{error}</span>
            </div>
          </div>
        )}

        {/* Jobs List */}
        {!loading && !error && (
          <>
            <p className="mb-4 text-gray-600">{filteredJobs.length} jobs found</p>
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {filteredJobs.map((job, index) => (
                <div key={index} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                  <div className="p-6">
                    <h2 className="text-xl font-semibold text-gray-900 mb-2">{job.job_title}</h2>
                    <p className="text-blue-600 font-medium mb-2">{job.company_name}</p>
                    <p className="text-gray-600 mb-4">{job.job_location}</p>
                    
                    <div className="mb-4">
                      <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full mr-2 mb-2">
                        {job.job_schedule_type || 'Not specified'}
                      </span>
                      {job.job_work_from_home === 'Yes' && (
                        <span className="inline-block bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full mr-2 mb-2">
                          Remote
                        </span>
                      )}
                      {job.job_posted_date && (
                        <span className="inline-block bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded-full mb-2">
                          {job.job_posted_date}
                        </span>
                      )}
                    </div>
                    
                    {job.job_skills && (
                      <div className="mb-4">
                        <p className="text-sm text-gray-700 font-medium mb-1">Skills:</p>
                        <p className="text-sm text-gray-600">{job.job_skills}</p>
                      </div>
                    )}
                    
                    <div className="mt-4 flex justify-end">
                      <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors">
                        View Details
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            
            {filteredJobs.length === 0 && (
              <div className="text-center py-12">
                <p className="text-gray-600">No jobs found matching your criteria.</p>
              </div>
            )}
          </>
        )}
        
        <div className="mt-8 text-center">
          <Link href="/" className="text-blue-600 hover:text-blue-800 font-medium">
            ← Back to Dashboard
          </Link>
        </div>
      </div>
    </div>
  );
}