import React, { useEffect, useState } from "react";
import { AlertCircle } from "lucide-react";

const ConditionInfoSection = ({ success, resultUrl, detections }) => {
  const [conditionInfo, setConditionInfo] = useState(null);
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState("");

  useEffect(() => {
    console.log("ConditionInfoSection props:", { success, resultUrl, detections });
    
    if (success && resultUrl && detections && detections.length > 0) {
      console.log("All conditions met, making API call");
      setLoading(true);
      setApiError("");
      const conditionName = detections[0].name;
      console.log("Condition name:", conditionName);
      
      fetch(
        `http://localhost:8000/condition-info?name=${encodeURIComponent(
          conditionName
        )}`
      )
        .then((res) => {
          console.log("Response status:", res.status);
          if (!res.ok) {
            console.log("Response not OK:", res.status, res.statusText);
            throw new Error("Failed to fetch condition info");
          }
          return res.json();
        })
        .then((data) => {
          console.log("API Response:", data);
          setConditionInfo(data);
        })
        .catch((error) => {
          console.log("API Error:", error);
          setApiError("Could not fetch condition information. Please try again later.");
        })
        .finally(() => setLoading(false));
    } else {
      console.log("Conditions not met:", { 
        success, 
        hasResultUrl: !!resultUrl, 
        hasDetections: !!detections, 
        detectionsLength: detections?.length 
      });
      setConditionInfo(null);
    }
  }, [success, resultUrl, detections]);

  // Function to clean the message text
  const cleanMessage = (message) => {
    if (!message) return "No information available.";
    
    // Remove "(50 words)" or similar patterns
    return message
      .replace(/\(50\s*words\)/gi, '')
      .replace(/\(under\s*50\s*words\)/gi, '')
      .replace(/\(keep\s*it\s*under\s*50\s*words\)/gi, '')
      .replace(/\(under\s*100\s*words\)/gi, '')
      .replace(/\(keep\s*it\s*under\s*100\s*words\)/gi, '')
      .trim();
  };

  return (
    <div className="bg-white rounded-xl shadow-xl p-4">
      <h2 className="text-xl font-semibold text-gray-800 mb-3 flex items-center">
        <AlertCircle className="mr-2 text-purple-600" size={20} />
        Condition Info
      </h2>
      
      {!success || !resultUrl ? (
        <div className="border-2 border-gray-200 rounded-xl p-6 text-center bg-gray-50">
          <div className="text-gray-400 mb-3">
            <AlertCircle size={32} className="mx-auto" />
          </div>
          <p className="text-sm font-medium text-gray-500 mb-1">
            No condition detected
          </p>
          <p className="text-sm text-gray-400 px-2">
            Complete analysis to see condition information
          </p>
        </div>
      ) : loading ? (
        <div className="text-center py-6">
          <div className="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-purple-600"></div>
          <span className="text-purple-600 text-sm ml-2">
            Loading condition info...
          </span>
        </div>
      ) : apiError ? (
        <div className="text-center py-6">
          <span className="text-red-600 text-sm">{apiError}</span>
        </div>
      ) : conditionInfo ? (
        <div className="space-y-3">
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
            <h3 className="font-semibold text-purple-800 mb-2 text-sm">
              {detections[0].name}
            </h3>
            <p className="text-purple-700 text-sm leading-relaxed">
              {cleanMessage(conditionInfo.message)}
            </p>
          </div>
          
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
            <h4 className="font-medium text-blue-800 text-sm mb-2">
              Confidence Level:
            </h4>
            <div className="flex items-center space-x-2">
              <div className="flex-1 bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-500 h-2 rounded-full"
                  style={{
                    width: `${Math.round(detections[0].confidence * 100)}%`,
                  }}
                ></div>
              </div>
              <span className="text-blue-700 text-sm font-medium">
                {Math.round(detections[0].confidence * 100)}%
              </span>
            </div>
          </div>
        </div>
      ) : (
        <div className="text-center py-6">
          <span className="text-gray-600 text-sm">
            No information available.
          </span>
        </div>
      )}
    </div>
  );
};

export default ConditionInfoSection;
