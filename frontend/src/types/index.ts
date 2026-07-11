// Village types
export interface Village {
  id: number;
  name: string;
  state: string;
  district: string;
  area_sqkm: number;
  population: number;
  boundary?: any;
  created_at: string;
  updated_at: string;
}

// Infrastructure types
export interface Infrastructure {
  id: number;
  village_id: number;
  type: string;
  name: string;
  location?: any;
  properties: Record<string, any>;
  created_at: string;
}

// Analysis result types
export interface AnalysisResult {
  id: number;
  village_id: number;
  analysis_type: string;
  result_data: Record<string, any>;
  created_at: string;
}

// AI prediction types
export interface AIPrediction {
  id: number;
  village_id: number;
  prediction_type: string;
  geometry?: any;
  confidence: number;
  metadata: Record<string, any>;
  created_at: string;
}
